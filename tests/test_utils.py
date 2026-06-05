import pytest
import json
import tempfile
import os
from unittest.mock import patch
from src.utils import load_transactions_from_json

def test_load_transactions_from_json_valid():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_data = [{"amount": 100, "currency": "USD"}, {"amount": 200, "currency": "EUR"}]
        json.dump(test_data, f)
        f.close()
        
        result = load_transactions_from_json(f.name)
        assert result == test_data
        os.unlink(f.name)

def test_load_transactions_from_json_empty():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')
        f.close()
        
        result = load_transactions_from_json(f.name)
        assert result == []
        os.unlink(f.name)

def test_load_transactions_from_json_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = load_transactions_from_json('non_existent.json')
        assert result == []

def test_load_transactions_from_json_invalid_json():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{invalid json}')
        f.close()
        
        result = load_transactions_from_json(f.name)
        assert result == []
        os.unlink(f.name)

def test_load_transactions_from_json_not_list():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"key": "value"}, f)
        f.close()
        
        result = load_transactions_from_json(f.name)
        assert result == []
        os.unlink(f.name)

def test_load_transactions_from_json_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('')
        f.close()
        
        result = load_transactions_from_json(f.name)
        assert result == []
        os.unlink(f.name)
