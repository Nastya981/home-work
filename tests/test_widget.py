import pytest
from src.widget import mask_account_card, get_date

def test_mask_account_card_card():
    """Тест маскирования номера карты"""
    result = mask_account_card("Visa 1234567890123456")
    assert result == "Visa 1234 56** **** 3456"

def test_mask_account_card_account():
    """Тест маскирования номера счета"""
    result = mask_account_card("Счет 12345678901234567890")
    assert result == "Счет **7890"

def test_mask_account_card_invalid():
    """Тест с неверным форматом"""
    result = mask_account_card("1234567890")
    assert "Неверный" in result

def test_get_date():
    """Тест получения даты из строки"""
    result = get_date("2019-07-03T18:35:29.512364")
    assert result == "03.07.2019"

def test_get_date_invalid():
    """Тест с неверным форматом даты"""
    result = get_date("invalid date")
    assert result == "Неверная дата"
