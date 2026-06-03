import re
from collections import Counter
from typing import Any, Dict, List

from src.logger_config import setup_logger

logger = setup_logger('process_operations')


def filter_operations_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по строке поиска в описании.
    Использует модуль re для поиска.

    Args:
        transactions: Список словарей с операциями
        search_string: Строка для поиска

    Returns:
        Список отфильтрованных словарей
    """
    logger.info(f"Фильтрация операций по строке: '{search_string}'")

    if not transactions:
        logger.warning("Список операций пуст")
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
                logger.debug(f"Найдено совпадение: {description[:50]}...")

        logger.info(f"Найдено {len(result)} операций по строке '{search_string}'")
        return result

    except re.error as e:
        logger.error(f"Ошибка регулярного выражения: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return []


def count_operations_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.
    Использует Counter из библиотеки collections.

    Args:
        transactions: Список операций
        categories: Список категорий

    Returns:
        Словарь с количеством операций по категориям
    """
    logger.info(f"Подсчёт операций по категориям: {categories}")

    if not transactions:
        logger.warning("Список операций пуст")
        return {category: 0 for category in categories} if categories else {}

    if not categories:
        logger.warning("Список категорий пуст")
        return {}

    category_counts = Counter()

    for transaction in transactions:
        description = transaction.get('description', '')
        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                category_counts[category] += 1
                logger.debug(f"Операция отнесена к категории '{category}'")
                break

    result = {category: category_counts.get(category, 0) for category in categories}
    logger.info(f"Результат подсчёта: {result}")
    return result
