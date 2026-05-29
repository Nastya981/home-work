from typing import Dict, Any, Optional
import requests
import logging
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настраиваем логгер для модуля external_api
logger = logging.getLogger('external_api')
logger.setLevel(logging.DEBUG)

# Создаём папку logs если её нет
os.makedirs('logs', exist_ok=True)

# Настраиваем file_handler
file_handler = logging.FileHandler('logs/external_api.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настраиваем формат
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)

# API ключ из .env
API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
_currency_cache: Dict[str, float] = {}


def get_exchange_rate(from_currency: str) -> Optional[float]:
    """Получает курс валюты к рублю через внешнее API"""
    logger.info(f"Запрос курса {from_currency} к RUB")

    if from_currency in _currency_cache:
        rate = _currency_cache[from_currency]
        logger.debug(f"Курс {from_currency} = {rate} (из кэша)")
        return rate

    try:
        logger.debug(f"Отправка запроса к API для {from_currency}")
        
        # Используем API ключ в headers (как требует документация)
        if API_KEY:
            headers = {'apikey': API_KEY}
            url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols=RUB"
            response = requests.get(url, headers=headers, timeout=10)
        else:
            # Fallback на бесплатный API если ключа нет
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}", timeout=10)
        
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        if 'rates' in data and 'RUB' in data['rates']:
            rate_value = data['rates']['RUB']
            rate = float(rate_value)
            _currency_cache[from_currency] = rate
            logger.info(f"Получен курс {from_currency} = {rate} RUB")
            return rate
        else:
            logger.error(f"Не удалось получить курс {from_currency}: ответ API не содержит RUB")
            return None
    except Exception as e:
        logger.error(f"Ошибка при запросе курса {from_currency}: {e}")
        return None


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли"""
    logger.debug(f"Начало конвертации транзакции: {transaction.get('description', 'Unknown')}")

    if 'operationAmount' not in transaction:
        logger.error("В транзакции отсутствует поле operationAmount")
        raise ValueError("Нет поля operationAmount")

    operation_amount = transaction['operationAmount']
    amount = operation_amount.get('amount')
    currency = operation_amount.get('currency', {}).get('code')

    if amount is None or currency is None:
        logger.error(f"Отсутствуют поля amount или currency: amount={amount}, currency={currency}")
        raise ValueError("Нет полей amount или currency в operationAmount")

    try:
        amount_float = float(amount)
        logger.debug(f"Сумма: {amount_float} {currency}")
    except (ValueError, TypeError) as e:
        logger.error(f"Некорректная сумма: {amount} - {e}")
        raise ValueError(f"Некорректная сумма: {amount}")

    if str(currency).upper() == 'RUB':
        logger.info(f"Конвертация не требуется: {amount_float} RUB")
        return amount_float

    if str(currency).upper() in ['USD', 'EUR']:
        rate = get_exchange_rate(str(currency).upper())
        if rate is not None:
            result = amount_float * rate
            logger.info(f"Конвертация: {amount_float} {currency} = {result:.2f} RUB")
            return result
        else:
            logger.warning(f"Не удалось конвертировать {currency}, возвращаем 0")

    logger.warning(f"Валюта {currency} не поддерживается")
    return 0.0
