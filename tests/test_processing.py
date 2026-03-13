"""
Тесты для модуля processing.py.
"""
import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_by_state_default(self):
        """Тестирование фильтрации со статусом по умолчанию."""
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
            {"id": 3, "state": "EXECUTED", "date": "2024-01-03"},
        ]
        result = filter_by_state(data)
        assert len(result) == 2
        assert all(item["state"] == "EXECUTED" for item in result)

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 0),
    ])
    def test_filter_by_state_different(self, state, expected_count):
        """Тестирование фильтрации с разными статусами."""
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
            {"id": 3, "state": "CANCELED", "date": "2024-01-03"},
        ]
        result = filter_by_state(data, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(item["state"] == state for item in result)

    def test_filter_by_state_empty(self):
        """Тестирование с пустым списком."""
        assert filter_by_state([]) == []


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(self):
        """Тестирование сортировки по убыванию."""
        data = [
            {"id": 1, "date": "2024-01-03"},
            {"id": 2, "date": "2024-01-01"},
            {"id": 3, "date": "2024-01-02"},
        ]
        result = sort_by_date(data)
        dates = [item["date"] for item in result]
        assert dates == ["2024-01-03", "2024-01-02", "2024-01-01"]

    def test_sort_by_date_ascending(self):
        """Тестирование сортировки по возрастанию."""
        data = [
            {"id": 1, "date": "2024-01-03"},
            {"id": 2, "date": "2024-01-01"},
            {"id": 3, "date": "2024-01-02"},
        ]
        result = sort_by_date(data, reverse=False)
        dates = [item["date"] for item in result]
        assert dates == ["2024-01-01", "2024-01-02", "2024-01-03"]

    def test_sort_by_date_same_dates(self):
        """Тестирование сортировки с одинаковыми датами."""
        data = [
            {"id": 1, "date": "2024-01-01"},
            {"id": 2, "date": "2024-01-01"},
            {"id": 3, "date": "2024-01-02"},
        ]
        result = sort_by_date(data)
        # При сортировке по убыванию, более поздняя дата должна быть первой
        assert result[0]["date"] == "2024-01-02"
        assert result[1]["date"] == "2024-01-01"
        assert result[2]["date"] == "2024-01-01"

    def test_sort_by_date_empty(self):
        """Тестирование сортировки пустого списка."""
        assert sort_by_date([]) == []
