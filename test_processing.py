"""
Тесты для модуля processing.
"""

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed():
    """
    Тест фильтрации операций со статусом EXECUTED.
    """
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    expected = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    result = filter_by_state(operations)

    assert result == expected, f"Ожидалось {expected}, получено {result}"
    assert len(result) == 2, f"Ожидалось 2 операции, получено {len(result)}"


def test_filter_by_state_canceled():
    """
    Тест фильтрации операций со статусом CANCELED.
    """
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    expected = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    result = filter_by_state(operations, "CANCELED")

    assert result == expected, f"Ожидалось {expected}, получено {result}"
    assert len(result) == 2, f"Ожидалось 2 операции, получено {len(result)}"


def test_filter_by_state_empty_result():
    """
    Тест фильтрации, когда нет операций с указанным статусом.
    """
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    result = filter_by_state(operations, "CANCELED")

    assert result == [], f"Ожидался пустой список, получено {result}"


def test_filter_by_state_empty_input():
    """
    Тест фильтрации с пустым входным списком.
    """
    result = filter_by_state([])
    assert result == [], "При пустом входном списке должен возвращаться пустой список"


def test_sort_by_date_descending():
    """
    Тест сортировки операций по дате по убыванию (сначала новые).
    """
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    expected = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]

    result = sort_by_date(operations)

    assert result == expected, f"Ожидалось {expected}, получено {result}"
    # Проверяем, что первая операция - самая новая
    assert result[0]["date"] == "2019-07-03T18:35:29.512364", "Первая должна быть самая новая операция"
    # Проверяем, что последняя - самая старая
    assert result[-1]["date"] == "2018-06-30T02:08:58.425572", "Последняя должна быть самая старая операция"


def test_sort_by_date_ascending():
    """
    Тест сортировки операций по дате по возрастанию (сначала старые).
    """
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    expected = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]

    result = sort_by_date(operations, reverse=False)

    assert result == expected, f"Ожидалось {expected}, получено {result}"
    # Проверяем, что первая операция - самая старая
    assert result[0]["date"] == "2018-06-30T02:08:58.425572", "Первая должна быть самая старая операция"
    # Проверяем, что последняя - самая новая
    assert result[-1]["date"] == "2019-07-03T18:35:29.512364", "Последняя должна быть самая новая операция"


def test_sort_by_date_same_dates():
    """
    Тест сортировки операций с одинаковыми датами.
    """
    operations = [
        {"id": 1, "date": "2023-01-01T12:00:00"},
        {"id": 2, "date": "2023-01-01T12:00:00"},
        {"id": 3, "date": "2023-01-01T12:00:00"},
    ]

    result = sort_by_date(operations)

    # При одинаковых датах порядок может быть любым, главное - не изменилось количество
    assert len(result) == 3, "Длина списка не должна измениться"
    assert all(op["date"] == "2023-01-01T12:00:00" for op in result), "Все даты должны остаться одинаковыми"


def test_sort_by_date_empty_input():
    """
    Тест сортировки с пустым входным списком.
    """
    result = sort_by_date([])
    assert result == [], "При пустом входном списке должен возвращаться пустой список"


def test_sort_by_date_single_element():
    """
    Тест сортировки списка с одним элементом.
    """
    operations = [{"id": 1, "date": "2023-01-01T12:00:00"}]
    result = sort_by_date(operations)
    assert result == operations, "Список с одним элементом не должен измениться"


if __name__ == "__main__":
    # Ручной запуск тестов для демонстрации
    print("Запуск тестов...")
    test_filter_by_state_executed()
    test_filter_by_state_canceled()
    test_filter_by_state_empty_result()
    test_filter_by_state_empty_input()
    test_sort_by_date_descending()
    test_sort_by_date_ascending()
    test_sort_by_date_same_dates()
    test_sort_by_date_empty_input()
    test_sort_by_date_single_element()
    print("Все тесты пройдены!")
