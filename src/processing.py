"""Модуль для обработки списка транзакций."""

from typing import Dict, List, Any


def filter_by_state(
    transactions: List[Dict[str, Any]],
    state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по заданному статусу.

    Параметры:
        transactions: список словарей с транзакциями
        state: статус для фильтрации (по умолчанию "EXECUTED")

    Возвращает:
        отфильтрованный список транзакций
    """
    return [item for item in transactions if item.get("state") == state]


def sort_by_date(
    transactions: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список транзакций по дате.

    Параметры:
        transactions: список словарей с транзакциями
        reverse: если True - сортировка по убыванию, если False - по возрастанию

    Возвращает:
        отсортированный список транзакций
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)

