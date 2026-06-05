import csv
from typing import List, Dict, Any, Optional
from src.logger_config import setup_logger

logger = setup_logger('file_reader')


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла
    Использует встроенный модуль csv

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    try:
        transactions = []

        # Используем utf-8-sig для удаления BOM
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            # Определяем разделитель (запятая или точка с запятой)
            sample = file.read(1024)
            file.seek(0)
            delimiter = ';' if ';' in sample else ','

            logger.debug(f"Определён разделитель: '{delimiter}'")

            # Используем csv.DictReader
            reader = csv.DictReader(file, delimiter=delimiter)

            for row in reader:
                # Преобразуем типы данных
                cleaned_row = {}
                for key, value in row.items():
                    # Удаляем возможные пробелы
                    if isinstance(value, str):
                        value = value.strip()

                    # Пробуем преобразовать в число, если возможно
                    if value is None or value == '':
                        cleaned_row[key] = None
                    elif value.isdigit():
                        cleaned_row[key] = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                        cleaned_row[key] = float(value)
                    else:
                        cleaned_row[key] = value
                transactions.append(cleaned_row)

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        if transactions:
            logger.debug(f"Первая транзакция: {transactions[0]}")
        return transactions

    except FileNotFoundError as e:
        logger.error(f"CSV-файл не найден: {file_path}. Ошибка: {e}")
        return []
    except csv.Error as e:
        logger.error(f"Ошибка CSV: {e}")
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
        import pandas as pd
        df = pd.read_excel(file_path, engine='openpyxl')

        if df.empty:
            logger.warning(f"Excel-файл {file_path} пуст")
            return []

        # Преобразуем типы данных
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
            elif df[col].dtype in ['int64', 'float64']:
                pass

        transactions = df.to_dict(orient='records')

        # Обрабатываем NaN значения
        for transaction in transactions:
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None
                elif isinstance(value, str):
                    # Пробуем преобразовать строки в числа
                    if value.isdigit():
                        transaction[key] = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                        transaction[key] = float(value)

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
        if transactions:
            logger.debug(f"Первая транзакция: {transactions[0]}")
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

    if file_path.lower().endswith('.csv'):
        logger.debug("Определён формат CSV")
        return read_csv_transactions(file_path)
    elif file_path.lower().endswith('.xlsx'):
        logger.debug("Определён формат Excel")
        return read_excel_transactions(file_path)
    else:
        logger.error(f"Неподдерживаемый формат файла: {file_path}")
        return None
