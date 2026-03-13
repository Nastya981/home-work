"""
Модуль для работы с виджетами банковских операций.
"""


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер счета или карты.

    Параметры:
        account_info: строка с типом и номером счета/карты

    Возвращает:
        строку с замаскированным номером
    """
    parts = account_info.rsplit(' ', 1)
    if len(parts) != 2:
        return account_info

    account_type = parts[0]
    number = parts[1]

    if len(number) == 16:  # карта
        masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    else:  # счет
        masked = f"**{number[-4:]}"

    return f"{account_type} {masked}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Параметры:
        date_str: строка с датой в формате "YYYY-MM-DDTHH:MM:SS.mmmmmm"

    Возвращает:
        строку с датой в формате "ДД.ММ.ГГГГ"
    """
    if not date_str:
        return ""

    date_part = date_str.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"


# tests/test_widget.py
import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции маскировки карты или счета"""

    @pytest.mark.parametrize("input_str, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ])
    def test_mask_account_card_valid(self, input_str, expected):
        """Проверка корректного распознавания типа и маскировки"""
        assert mask_account_card(input_str) == expected

    @pytest.mark.parametrize("input_str", [
        "American Express 371449635398431",  # 15-значный номер
        "Visa 1234",  # слишком короткий номер
        "Счет 123",  # слишком короткий счет
        "Unknown 1234567890123456",  # неизвестный тип
        "",  # пустая строка
        "1234567890123456",  # без типа
    ])
    def test_mask_account_card_edge_cases(self, input_str):
        """Проверка граничных случаев"""
        # Функция не должна падать, но результат может быть разным
        result = mask_account_card(input_str)
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetDate:
    """Тесты для функции преобразования даты"""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T12:30:45.123456", "11.03.2024"),
        ("2024-03-11T12:30:45", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
    ])
    def test_get_date_valid(self, input_date, expected):
        """Тестирование правильности преобразования даты"""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize("input_date", [
        "11.03.2024",  # неверный формат
        "invalid date",
        "",
        "2024-13-45",  # некорректная дата
    ])
    def test_get_date_invalid(self, input_date):
        """Проверка обработки некорректных форматов даты"""
        with pytest.raises((ValueError, IndexError)):
            get_date(input_date)