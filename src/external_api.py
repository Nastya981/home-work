from typing import Dict, Any, Optional
import requests

_currency_cache: Dict[str, float] = {}

def get_exchange_rate(from_currency: str) -> Optional[float]:
    """олучает курс валюты к рублю через внешнее API"""
    if from_currency in _currency_cache:
        return _currency_cache[from_currency]
    
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}", timeout=10)
        data = response.json()
        
        if 'rates' in data and 'RUB' in data['rates']:
            rate = data['rates']['RUB']
            _currency_cache[from_currency] = rate
            return rate
        return None
    except Exception:
        return None

def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """онвертирует сумму транзакции в рубли"""
    # роверяем наличие полей
    if 'operationAmount' not in transaction:
        raise ValueError("ет поля operationAmount")
    
    operation_amount = transaction['operationAmount']
    amount = operation_amount.get('amount')
    currency = operation_amount.get('currency', {}).get('code')
    
    if amount is None or currency is None:
        raise ValueError("ет полей amount или currency в operationAmount")
    
    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        raise ValueError(f"екорректная сумма: {amount}")
    
    if currency.upper() == 'RUB':
        return amount_float
    
    if currency.upper() in ['USD', 'EUR']:
        rate = get_exchange_rate(currency.upper())
        if rate:
            return amount_float * rate
    
    return 0.0
