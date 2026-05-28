from typing import Dict, Any, Optional
import requests
from src.logger_config import setup_logger

# астраиваем логгер для модуля external_api
logger = setup_logger('external_api')

_currency_cache: Dict[str, float] = {}

def get_exchange_rate(from_currency: str) -> Optional[float]:
    """олучает курс валюты к рублю через внешнее API"""
    logger.info(f"апрос курса {from_currency} к RUB")
    
    if from_currency in _currency_cache:
        rate: float = _currency_cache[from_currency]
        logger.debug(f"урс {from_currency} = {rate} (из кэша)")
        return rate
    
    try:
        logger.debug(f"тправка запроса к API для {from_currency}")
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}", timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        
        if 'rates' in data and 'RUB' in data['rates']:
            rate_value = data['rates']['RUB']
            # риводим к float явно
            if isinstance(rate_value, (int, float)):
                rate = float(rate_value)
            elif isinstance(rate_value, str):
                rate = float(rate_value)
            else:
                rate = 0.0
            _currency_cache[from_currency] = rate
            logger.info(f"олучен курс {from_currency} = {rate} RUB")
            return rate
        else:
            logger.error(f"е удалось получить курс {from_currency}: ответ API не содержит RUB")
            return None
    except Exception as e:
        logger.error(f"шибка при запросе курса {from_currency}: {e}")
        return None

def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """онвертирует сумму транзакции в рубли"""
    logger.debug(f"ачало конвертации транзакции: {transaction.get('description', 'Unknown')}")
    
    if 'operationAmount' not in transaction:
        logger.error(" транзакции отсутствует поле operationAmount")
        raise ValueError("ет поля operationAmount")
    
    operation_amount: Dict[str, Any] = transaction['operationAmount']
    amount = operation_amount.get('amount')
    currency = operation_amount.get('currency', {}).get('code')
    
    if amount is None or currency is None:
        logger.error(f"тсутствуют поля amount или currency: amount={amount}, currency={currency}")
        raise ValueError("ет полей amount или currency в operationAmount")
    
    try:
        amount_float: float = float(amount)
        logger.debug(f"Сумма: {amount_float} {currency}")
    except (ValueError, TypeError) as e:
        logger.error(f"екорректная сумма: {amount} - {e}")
        raise ValueError(f"екорректная сумма: {amount}")
    
    if str(currency).upper() == 'RUB':
        logger.info(f"онвертация не требуется: {amount_float} RUB")
        return amount_float
    
    if str(currency).upper() in ['USD', 'EUR']:
        rate: Optional[float] = get_exchange_rate(str(currency).upper())
        if rate is not None:
            result: float = amount_float * rate
            logger.info(f"онвертация: {amount_float} {currency} = {result:.2f} RUB")
            return result
        else:
            logger.warning(f"е удалось конвертировать {currency}, возвращаем 0")
    
    logger.warning(f"алюта {currency} не поддерживается")
    return 0.0
