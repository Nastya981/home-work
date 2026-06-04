import pytest
from src.process_operations import filter_operations_by_description, count_operations_by_categories

test_transactions = [
    {'id': 1, 'description': 'Перевод организации', 'state': 'EXECUTED'},
    {'id': 2, 'description': 'Перевод со счета на счет', 'state': 'CANCELED'},
    {'id': 3, 'description': 'Открытие вклада', 'state': 'EXECUTED'},
    {'id': 4, 'description': 'Оплата услуг', 'state': 'PENDING'},
]


def test_filter_operations_by_description():
    """Тест фильтрации по описанию"""
    result = filter_operations_by_description(test_transactions, 'Перевод')
    assert len(result) == 2
    assert all('Перевод' in t['description'] for t in result)


def test_filter_operations_by_description_case_insensitive():
    """Тест регистронезависимого поиска"""
    result = filter_operations_by_description(test_transactions, 'перевод')
    assert len(result) == 2


def test_filter_operations_by_description_not_found():
    """Тест поиска отсутствующей строки"""
    result = filter_operations_by_description(test_transactions, 'Несуществующее')
    assert len(result) == 0


def test_filter_operations_by_description_empty_list():
    """Тест с пустым списком"""
    result = filter_operations_by_description([], 'Перевод')
    assert result == []


def test_count_operations_by_categories():
    """Тест подсчёта по категориям"""
    categories = ['Перевод', 'Открытие']
    result = count_operations_by_categories(test_transactions, categories)
    assert result['Перевод'] == 2
    assert result['Открытие'] == 1


def test_count_operations_by_categories_empty_list():
    """Тест подсчёта с пустым списком"""
    categories = ['Перевод']
    result = count_operations_by_categories([], categories)
    assert result['Перевод'] == 0


def test_count_operations_by_categories_empty_categories():
    """Тест с пустым списком категорий"""
    result = count_operations_by_categories(test_transactions, [])
    assert result == {}
