from typing import Dict, Any, Optional
import requests

_currency_cache: Dict[str, float] = {}

def get_exchange_rate(from_currency: str) -> Optional[float]:
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
    except:
        return None

def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    amount = transaction.get('amount')
    currency = transaction.get('currency')
    
    if amount is None or currency is None:
        raise ValueError("ет полей amount или currency")
    
    amount_float = float(amount)
    
    if currency.upper() == 'RUB':
        return amount_float
    
    if currency.upper() in ['USD', 'EUR']:
        rate = get_exchange_rate(currency.upper())
        if rate:
            return amount_float * rate
    
    return 0.0
