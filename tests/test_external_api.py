import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rubles, get_exchange_rate

def test_convert_to_rubles_rub():
    transaction = {
        "operationAmount": {
            "amount": "5000",
            "currency": {"code": "RUB"}
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 5000.0

def test_convert_to_rubles_usd():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }
    with patch('src.external_api.get_exchange_rate', return_value=95.0):
        result = convert_to_rubles(transaction)
        assert result == 9500.0

def test_convert_to_rubles_eur():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "EUR"}
        }
    }
    with patch('src.external_api.get_exchange_rate', return_value=105.0):
        result = convert_to_rubles(transaction)
        assert result == 10500.0

def test_convert_to_rubles_missing_fields():
    transaction = {"amount": 100}
    with pytest.raises(ValueError):
        convert_to_rubles(transaction)

def test_get_exchange_rate_with_mock():
    mock_response = Mock()
    mock_response.json.return_value = {'rates': {'RUB': 95.0}}
    
    with patch('src.external_api.requests.get', return_value=mock_response):
        result = get_exchange_rate('USD')
        assert result == 95.0
