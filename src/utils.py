import json
from typing import List, Dict, Any
from src.logger_config import setup_logger

# астраиваем логгер для модуля utils
logger = setup_logger('utils')

def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """агружает список транзакций из JSON-файла"""
    logger.info(f"ачало загрузки транзакций из файла: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            if isinstance(data, list):
                logger.info(f"спешно загружено {len(data)} транзакций")
                logger.debug(f"ервая транзакция: {data[0] if data else 'None'}")
                return data
            else:
                logger.error(f"анные не являются списком: {type(data)}")
                return []
                
    except FileNotFoundError as e:
        logger.error(f"айл не найден: {file_path} - {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"шибка декодирования JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"еожиданная ошибка: {e}")
        return []
