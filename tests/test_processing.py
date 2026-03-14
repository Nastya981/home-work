"""Тесты для модуля processing."""

import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции фильтрации по статусу."""

    def test_filter_by_state_default(self, sample_transactions):
        """Тестирование фильтрации со статусом по умолчанию (EXECUTED)."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 5
        assert all(item["state"] == "EXECUTED" for item in result)

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 5),
            ("CANCELED", 2),
            ("PENDING", 1),
            ("UNKNOWN", 0),
        ],
    )
    def test_filter_by_state_different_states(self, sample_transactions, state, expected_count):
        """Параметризованный тест для разных статусов."""
        result = filter_by_state(sample_transactions, state)
        if expected_count > 0:
            assert all(item["state"] == state for item in result)
        assert len(result) == expected_count

    def test_filter_by_state_empty_list(self):
        """Проверка работы с пустым списком."""
        assert filter_by_state([]) == []

    def test_filter_by_state_no_state_key(self):
        """Проверка обработки словарей без ключа state."""
        data = [{"id": 1}, {"id": 2, "state": "EXECUTED"}]
        result = filter_by_state(data)
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для функции сортировки по дате."""

    def test_sort_by_date_descending(self, sample_transactions):
        """Тестирование сортировки по убыванию."""
        result = sort_by_date(sample_transactions)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_transactions):
        """Тестирование сортировки по возрастанию."""
        result = sort_by_date(sample_transactions, reverse=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_sort_by_date_same_dates(self, sample_transactions_with_same_dates):
        """Проверка сортировки при одинаковых датах."""
        result = sort_by_date(sample_transactions_with_same_dates)
        for i in range(len(result) - 1):
            if result[i]["date"] == result[i + 1]["date"]:
                assert result[i]["id"] < result[i + 1]["id"]

    @pytest.mark.parametrize("reverse", [True, False])
    def test_sort_by_date_empty_list(self, reverse):
        """Проверка сортировки пустого списка."""
        assert sort_by_date([], reverse) == []

    def test_sort_by_date_invalid_dates(self):
        """Проверка обработки некорректных форматов дат."""
        data = [
            {"date": "2024-03-11T12:30:45", "id": 1},
            {"date": "invalid", "id": 2},
            {"date": "2024-03-10", "id": 3},
        ]
        result = sort_by_date(data)
        assert len(result) == 3

    def test_sort_by_date_missing_date_key(self):
        """Проверка обработки отсутствия ключа date."""
        data = [{"id": 1}, {"date": "2024-03-11", "id": 2}]
        with pytest.raises(KeyError):
            sort_by_date(data)