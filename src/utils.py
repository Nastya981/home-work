import json
from typing import List, Dict, Any
import logging
import os


# Настраиваем логгер для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Создаём папку logs если её нет
os.makedirs('logs', exist_ok=True)

# Настраиваем file_handler
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настраиваем формат
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logger.debug(f"Файл {file_path} успешно открыт")
            data = json.load(file)
            logger.debug(f"JSON успешно декодирован, тип данных: {type(data)}")

            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций")
                if data:
                    logger.debug(f"Первая транзакция: {data[0]}")
                return data
            else:
                logger.error(f"Данные в файле не являются списком. Фактический тип: {type(data)}")
                return []

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {file_path}. Ошибка: {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}. Ошибка: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {e}")
        return []
