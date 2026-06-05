import pytest
import pandas as pd
import os
import tempfile
from unittest.mock import patch, Mock
from src.file_reader import read_csv_transactions, read_excel_transactions, detect_and_read_file


def test_read_csv_transactions_valid():
    """Тест чтения валидного CSV-файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('id,amount,currency,description\n')
        f.write('1,100,USD,Online purchase\n')
        f.write('2,250,EUR,Restaurant payment\n')
        f.close()

        result = read_csv_transactions(f.name)
        assert len(result) == 2
        assert result[0]['amount'] == 100
        assert result[0]['currency'] == 'USD'
        os.unlink(f.name)


def test_read_csv_transactions_empty():
    """Тест чтения пустого CSV-файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('id,amount,currency,description\n')
        f.close()

        result = read_csv_transactions(f.name)
        assert result == []
        os.unlink(f.name)


def test_read_csv_transactions_not_found():
    """Тест чтения несуществующего CSV-файла"""
    result = read_csv_transactions('non_existent.csv')
    assert result == []


def test_read_excel_transactions_valid():
    """Тест чтения валидного Excel-файла"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        # Создаём тестовый Excel файл
        df = pd.DataFrame({
            'id': [1, 2],
            'amount': [100, 250],
            'currency': ['USD', 'EUR'],
            'description': ['Online purchase', 'Restaurant payment']
        })
        df.to_excel(f.name, index=False, engine='openpyxl')
        f.close()

        result = read_excel_transactions(f.name)
        assert len(result) == 2
        assert result[0]['amount'] == 100
        assert result[0]['currency'] == 'USD'
        os.unlink(f.name)


def test_detect_and_read_file_csv():
    """Тест автоматического определения CSV-файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('id,amount,currency\n')
        f.write('1,100,USD\n')
        f.close()

        result = detect_and_read_file(f.name)
        assert result is not None
        assert len(result) == 1
        os.unlink(f.name)


def test_detect_and_read_file_xlsx():
    """Тест автоматического определения Excel-файла"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame({'id': [1], 'amount': [100], 'currency': ['USD']})
        df.to_excel(f.name, index=False, engine='openpyxl')
        f.close()

        result = detect_and_read_file(f.name)
        assert result is not None
        assert len(result) == 1
        os.unlink(f.name)


def test_detect_and_read_file_unsupported():
    """Тест неподдерживаемого формата"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write('test data'.encode())
        f.close()

        result = detect_and_read_file(f.name)
        assert result is None
        os.unlink(f.name)
