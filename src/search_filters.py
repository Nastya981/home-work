import re
from typing import Any, Dict, List

from src.logger_config import setup_logger

# Настраиваем логгер
logger = setup_logger('search_filters')


def search_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Ищет транзакции, содержащие заданную строку в описании."""
    logger.info(f"Поиск транзакций по строке: '{search_string}'")

    if not transactions:
        logger.warning("Список транзакций пуст")
        return []

    if not search_string:
        logger.warning("Строка поиска пуста")
        return []

    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        result = []

        for transaction in transactions:
            description = transaction.get('description', '')
            if pattern.search(str(description)):
                result.append(transaction)
                logger.debug("Найдено совпадение: " + description[:50] + "...")

        logger.info("Найдено " + str(len(result)) + " транзакций по строке '" + search_string + "'")
        return result

    except re.error as e:
        logger.error("Ошибка регулярного выражения: " + str(e))
        return []
    except Exception as e:
        logger.error("Неожиданная ошибка при поиске: " + str(e))
        return []


def count_transactions_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций в каждой категории."""
    logger.info("Подсчёт транзакций по категориям: " + str(categories))

    if not transactions:
        logger.warning("Список транзакций пуст")
        return {category: 0 for category in categories}

    if not categories:
        logger.warning("Список категорий пуст")
        return {}

    result = {category: 0 for category in categories}

    for transaction in transactions:
        description = transaction.get('description', '')
        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                result[category] += 1
                logger.debug("Транзакция отнесена к категории " + category + ": " + description[:50] + "...")
                break

    logger.info("Результат подсчёта: " + str(result))
    return result


def filter_by_state(transactions: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    logger.info("Фильтрация транзакций по статусу: " + state)

    if not transactions:
        logger.warning("Список транзакций пуст")
        return []

    state_upper = state.upper()
    valid_states = {'EXECUTED', 'CANCELED', 'PENDING'}

    if state_upper not in valid_states:
        logger.error("Некорректный статус: " + state)
        raise ValueError("Некорректный статус операции. Доступные статусы: EXECUTED, CANCELED, PENDING")

    result = [t for t in transactions if t.get('state', '').upper() == state_upper]
    logger.info("Отфильтровано " + str(len(result)) + " транзакций по статусу " + state)
    return result


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str = 'RUB') -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте."""
    logger.info("Фильтрация транзакций по валюте: " + currency)

    if not transactions:
        return []

    currency_upper = currency.upper()
    result = []

    for transaction in transactions:
        operation_amount = transaction.get('operationAmount', {})
        transaction_currency = operation_amount.get('currency', {}).get('code', '')
        if transaction_currency.upper() == currency_upper:
            result.append(transaction)

    logger.info("Отфильтровано " + str(len(result)) + " транзакций по валюте " + currency)
    return result
