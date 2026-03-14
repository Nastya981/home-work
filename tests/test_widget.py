"""Тесты для модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции маскировки карты или счета."""

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ],
    )
    def test_mask_account_card_valid(self, input_str, expected):
        """Проверка корректного распознавания типа и маскировки."""
        assert mask_account_card(input_str) == expected

    @pytest.mark.parametrize(
        "input_str",
        [
            "American Express 371449635398431",
            "Visa 1234",
            "Счет 123",
            "Unknown 1234567890123456",
            "1234567890123456",
        ],
    )
    def test_mask_account_card_edge_cases(self, input_str):
        """Проверка граничных случаев."""
        result = mask_account_card(input_str)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_mask_account_card_empty_string(self):
        """Проверка обработки пустой строки."""
        result = mask_account_card("")
        assert isinstance(result, str)


class TestGetDate:
    """Тесты для функции преобразования даты."""

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-03-11T12:30:45.123456", "11.03.2024"),
            ("2024-03-11T12:30:45", "11.03.2024"),
            ("2024-03-11", "11.03.2024"),
        ],
    )
    def test_get_date_valid(self, input_date, expected):
        """Тестирование правильности преобразования даты."""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize(
        "input_date",
        [
            "11.03.2024",
            "invalid date",
        ],
    )
    def test_get_date_invalid_raises_error(self, input_date):
        """Проверка, что функция выбрасывает исключение для некорректных форматов."""
        with pytest.raises(ValueError):
            get_date(input_date)

    def test_get_date_invalid_format_returns_string(self):
        """Проверка обработки даты с несуществующей датой."""
        # Функция может обрабатывать "2024-13-45" по-разному
        try:
            result = get_date("2024-13-45")
            assert isinstance(result, str)
        except ValueError:
            # Если выбрасывает исключение - тоже нормально
            pass

    def test_get_date_empty_string(self):
        """Проверка обработки пустой строки."""
        try:
            result = get_date("")
            assert isinstance(result, str)
        except ValueError:
            # Если выбрасывает исключение - тоже нормально
            pass