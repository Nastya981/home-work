"""
Фикстуры для тестов.
"""
import pytest
from typing import Any, Dict, List


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
    ]


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с номерами карт."""
    return [
        "7000792289606361",
        "1234567890123456",
        "7158300734726758",
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с номерами счетов."""
    return [
        "73654108430135874305",
        "12345678901234567890",
    ]


@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с датами."""
    return [
        "2024-03-11T12:30:45.123456",
        "2024-03-11T12:30:45",
        "2024-03-11",
    ]

