import json
from typing import List, Dict, Any

def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """агружает список транзакций из JSON-файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return []
