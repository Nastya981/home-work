"""
Тесты для модуля masks.py.
"""
import pytest
from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для функции маскировки номера карты."""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("7158300734726758", "7158 30** **** 6758"),
    ])
    def test_mask_card_number_valid(self, card_number, expected):
        """Тестирование правильности маскирования номера карты."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("card_number", [
        "1234",
        "12345678901234567890",
        "",
        "   ",
        "abcd efgh ijkl mnop",
    ])
    def test_mask_card_number_invalid(self, card_number):
        """Тестирование некорректных входных данных."""
        with pytest.raises(ValueError, match="должен состоять из 16 цифр"):
            get_mask_card_number(card_number)

    def test_mask_card_number_with_spaces_valid(self):
        """Проверка обработки номеров с пробелами."""
        result = get_mask_card_number("7000 7922 8960 6361")
        assert result == "7000 79** **** 6361"


class TestGetMaskAccount:
    """Тесты для функции маскировки номера счета."""

    @pytest.mark.parametrize("account_number, expected", [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("123456789012345678901234", "**1234"),
        ("123456", "**3456"),
    ])
    def test_mask_account_valid(self, account_number, expected):
        """Тестирование правильности маскирования номера счета."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize("account_number", [
        "",
        "   ",
        "abcd",
        "12",
    ])
    def test_mask_account_invalid(self, account_number):
        """Тестирование некорректных входных данных."""
        with pytest.raises(ValueError):
            get_mask_account(account_number)

    def test_mask_account_with_spaces(self):
        """Проверка обработки номеров с пробелами."""
        assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"

