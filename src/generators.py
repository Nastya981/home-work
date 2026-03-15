"""
Модуль с генераторами для обработки транзакций.
Содержит функции для фильтрации по валюте, получения описаний и генерации номеров карт.
"""

from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str = "USD"
) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список транзакций
        currency: Код валюты для фильтрации (по умолчанию USD)

    Returns:
        Генератор, возвращающий транзакции с указанной валютой

    Yields:
        Транзакции, соответствующие критерию фильтрации

    Пример:
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> for _ in range(2):
        ...     print(next(usd_transactions))
    """
    for transaction in transactions:
        try:
            transaction_currency = (
                transaction.get("operationAmount", {})
                .get("currency", {})
                .get("code", "")
            )
            if transaction_currency == currency:
                yield transaction
        except (AttributeError, KeyError, TypeError):
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(
    transactions: List[Dict[str, Any]]
) -> Generator[str, None, None]:
    """
    Возвращает описания транзакций по очереди.

    Args:
        transactions: Список транзакций

    Returns:
        Генератор, возвращающий описания транзакций

    Yields:
        Описание каждой транзакции

    Пример:
        >>> descriptions = transaction_descriptions(transactions)
        >>> for _ in range(5):
        ...     print(next(descriptions))
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
        except (AttributeError, KeyError, TypeError):
            # Пропускаем транзакции без описания или с некорректной структурой
            continue


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение диапазона
        end: Конечное значение диапазона

    Returns:
        Генератор, возвращающий номера карт в формате XXXX XXXX XXXX XXXX

    Yields:
        Номер карты в отформатированном виде

    Пример:
        >>> for card_number in card_number_generator(1, 5):
        ...     print(card_number)
    """
    if start < 1:
        start = 1
    if end > 9999999999999999:
        end = 9999999999999999

    for number in range(start, end + 1):
        # Форматируем номер: дополняем нулями до 16 цифр и добавляем пробелы
        card_str = str(number).zfill(16)
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted
