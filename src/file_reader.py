import pandas as pd
from typing import List, Dict, Any, Optional
import logging
import os
from src.logger_config import setup_logger

# Настраиваем логгер
logger = setup_logger('file_reader')


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    try:
        # Читаем CSV файл
        df = pd.read_csv(file_path)

        # Проверяем, что файл не пустой
        if df.empty:
            logger.warning(f"CSV-файл {file_path} пуст")
            return []

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')

        # Приводим типы данных
        for transaction in transactions:
            # Преобразуем NaN в None
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        logger.debug(f"Первая транзакция: {transactions[0] if transactions else 'None'}")
        return transactions

    except FileNotFoundError as e:
        logger.error(f"CSV-файл не найден: {file_path}. Ошибка: {e}")
        return []
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV-файл пуст: {file_path}. Ошибка: {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла (XLSX)

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    logger.info(f"Начало чтения Excel-файла: {file_path}")

    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path, engine='openpyxl')

        # Проверяем, что файл не пустой
        if df.empty:
            logger.warning(f"Excel-файл {file_path} пуст")
            return []

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')

        # Приводим типы данных
        for transaction in transactions:
            # Преобразуем NaN в None
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
        logger.debug(f"Первая транзакция: {transactions[0] if transactions else 'None'}")
        return transactions

    except FileNotFoundError as e:
        logger.error(f"Excel-файл не найден: {file_path}. Ошибка: {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel-файла {file_path}: {e}")
        return []


def detect_and_read_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Автоматически определяет тип файла по расширению и читает его

    Args:
        file_path: Путь к файлу

    Returns:
        Список транзакций или None, если формат не поддерживается
    """
    logger.info(f"Определение типа файла: {file_path}")

    if file_path.endswith('.csv'):
        logger.debug("Определён формат CSV")
        return read_csv_transactions(file_path)
    elif file_path.endswith('.xlsx'):
        logger.debug("Определён формат Excel")
        return read_excel_transactions(file_path)
    else:
        logger.error(f"Неподдерживаемый формат файла: {file_path}")
        return None
