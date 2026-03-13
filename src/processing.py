"""Модуль для обработки данных операций."""

from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по заданному состоянию.

    Параметры:
        operations: Список словарей с данными об операциях
        state: Значение для фильтрации по ключу 'state' (по умолчанию 'EXECUTED')

    Возвращает:
        Новый список, содержащий только операции с указанным состоянием
    """
    result = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    return result


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Параметры:
        operations: Список словарей с данными об операциях
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Возвращает:
        Новый отсортированный список
    """
    # Создаем копию списка
    sorted_operations = operations.copy()

    # Сортируем
    for i in range(len(sorted_operations)):
        for j in range(i + 1, len(sorted_operations)):
            # Сравниваем даты
            if reverse:
                # По убыванию (новые сначала)
                if sorted_operations[i].get("date", "") < sorted_operations[j].get("date", ""):
                    sorted_operations[i], sorted_operations[j] = sorted_operations[j], sorted_operations[i]
            else:
                # По возрастанию (старые сначала)
                if sorted_operations[i].get("date", "") > sorted_operations[j].get("date", ""):
                    sorted_operations[i], sorted_operations[j] = sorted_operations[j], sorted_operations[i]

    return sorted_operations

