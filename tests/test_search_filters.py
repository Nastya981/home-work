import pytest
from src.search_filters import search_transactions_by_description, count_transactions_by_categories, filter_by_state, filter_by_currency

# Тестовые данные
test_transactions = [
    {
        'id': 1,
        'description': 'Перевод организации',
        'state': 'EXECUTED',
        'operationAmount': {'amount': '100', 'currency': {'code': 'USD'}}
    },
    {
        'id': 2,
        'description': 'Перевод со счета на счет',
        'state': 'CANCELED',
        'operationAmount': {'amount': '250', 'currency': {'code': 'EUR'}}
    },
    {
        'id': 3,
        'description': 'Открытие вклада',
        'state': 'EXECUTED',
        'operationAmount': {'amount': '5000', 'currency': {'code': 'RUB'}}
    },
    {
        'id': 4,
        'description': 'Перевод с карты на карту',
        'state': 'PENDING',
        'operationAmount': {'amount': '50', 'currency': {'code': 'USD'}}
    }
]


def test_search_transactions_by_description():
    """Тест поиска по описанию"""
    result = search_transactions_by_description(test_transactions, 'Перевод')
    assert len(result) == 3
    assert all('Перевод' in t['description'] for t in result)


def test_search_transactions_by_description_case_insensitive():
    """Тест регистронезависимого поиска"""
    result = search_transactions_by_description(test_transactions, 'перевод')
    assert len(result) == 3


def test_search_transactions_by_description_not_found():
    """Тест поиска отсутствующей строки"""
    result = search_transactions_by_description(test_transactions, 'Несуществующее слово')
    assert len(result) == 0


def test_search_transactions_empty_list():
    """Тест поиска в пустом списке"""
    result = search_transactions_by_description([], 'test')
    assert result == []


def test_count_transactions_by_categories():
    """Тест подсчёта по категориям"""
    categories = ['Перевод', 'Открытие']
    result = count_transactions_by_categories(test_transactions, categories)
    assert result['Перевод'] == 3
    assert result['Открытие'] == 1


def test_filter_by_state():
    """Тест фильтрации по статусу"""
    result = filter_by_state(test_transactions, 'EXECUTED')
    assert len(result) == 2
    assert all(t['state'] == 'EXECUTED' for t in result)


def test_filter_by_state_invalid():
    """Тест с некорректным статусом"""
    with pytest.raises(ValueError):
        filter_by_state(test_transactions, 'INVALID')


def test_filter_by_currency():
    """Тест фильтрации по валюте"""
    result = filter_by_currency(test_transactions, 'USD')
    assert len(result) == 2
