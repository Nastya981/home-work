"""
Тесты для модуля widget.py.
"""
import pytest
from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции маскировки карты/счета."""

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ])
    def test_mask_account_card_valid(self, input_data, expected):
        """Тестирование корректных данных."""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa 1234", "Visa **1234"),
        ("Счет 123", "Счет **123"),
        ("Unknown 1234567890123456", "Unknown 1234 56** **** 3456"),
    ])
    def test_mask_account_card_edge_cases(self, input_data, expected):
        """Тестирование граничных случаев."""
        result = mask_account_card(input_data)
        assert result == expected

    def test_mask_account_card_no_type(self):
        """Тестирование строки без типа."""
        input_data = "1234567890123456"
        result = mask_account_card(input_data)
        assert result == input_data

    def test_mask_account_card_empty(self):
        """Тестирование пустой строки."""
        input_data = ""
        result = mask_account_card(input_data)
        assert result == ""

    def test_mask_account_card_spaces_only(self):
        """Тестирование строки из пробелов."""
        input_data = "   "
        result = mask_account_card(input_data)
        assert result == "   **"


class TestGetDate:
    """Тесты для функции преобразования даты."""

    @pytest.mark.parametrize("input_data, expected", [
        ("2024-03-11T12:30:45.123456", "11.03.2024"),
        ("2024-03-11T12:30:45", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
    ])
    def test_get_date_valid(self, input_data, expected):
        """Тестирование корректных форматов даты."""
        assert get_date(input_data) == expected

    def test_get_date_invalid_format_dd_mm_yyyy(self):
        """Тестирование формата ДД.ММ.ГГГГ (должен вызывать ошибку)."""
        with pytest.raises(ValueError):
            get_date("11.03.2024")

    def test_get_date_invalid_string(self):
        """Тестирование некорректной строки."""
        with pytest.raises(ValueError):
            get_date("invalid date")

    def test_get_date_invalid_date(self):
        """Тестирование некорректной даты (13 месяц)."""
        result = get_date("2024-13-45")
        assert result == "45.13.2024"

    def test_get_date_empty_string(self):
        """Тестирование пустой строки."""
        result = get_date("")
        assert result == ""

    def test_get_date_no_t_separator(self):
        """Тестирование даты без T разделителя."""
        result = get_date("2024-03-11")
        assert result == "11.03.2024"

    def test_get_date_with_timezone(self):
        """Тестирование даты с часовым поясом."""
        result = get_date("2024-03-11T12:30:45+03:00")
        assert result == "11.03.2024"

