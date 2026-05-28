import logging
import os
from datetime import datetime

def setup_logger(module_name: str) -> logging.Logger:
    """астраивает логгер для указанного модуля"""
    
    # Создаём папку logs если её нет
    os.makedirs('logs', exist_ok=True)
    
    # Создаём логгер
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    
    # чищаем старые обработчики, чтобы логи не дублировались
    if logger.handlers:
        logger.handlers.clear()
    
    # Создаём обработчик для записи в файл
    log_file = f'logs/{module_name}.log'
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # ормат лога: время | модуль | уровень | сообщение
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # обавляем обработчик к логгеру
    logger.addHandler(file_handler)
    
    return logger
