"""Фикстуры для тестирования."""

from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с различными номерами карт для тестирования."""
    return [
        "7000792289606361",
        "1234567890123456",
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с различными номерами счетов для тестирования."""
    return [
        "73654108430135874305",
        "1234567890",
    ]


@pytest.fixture
def sample_card_account_data() -> List[str]:
    """Фикстура с различными типами карт и счетов."""
    return [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "MasterCard 7158300734726758",
        "Visa Classic 6831982476737658",
        "Счет 73654108430135874305",
        "Visa 1234567890123456",
    ]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T12:30:45.123456"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-10T10:15:30.789012"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-09T09:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2024-03-08T18:45:22.345678"},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-07T08:30:15.123456"},
        {"id": 6, "state": "EXECUTED", "date": "2023-12-31T23:59:59.999999"},
        {"id": 7, "state": "CANCELED", "date": "2024-03-06T14:20:10.987654"},
        {"id": 8, "state": "EXECUTED", "date": "2024-03-05T11:11:11.111111"},
    ]


@pytest.fixture
def sample_transactions_with_same_dates() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями, имеющими одинаковые даты."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T12:30:45.123456"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-11T12:30:45.123456"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-11T12:30:45.123456"},
        {"id": 4, "state": "PENDING", "date": "2024-03-10T18:45:22.345678"},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-10T18:45:22.345678"},
    ]