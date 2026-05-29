import pytest
import os
import logging
import time
from src.logger_config import setup_logger

def test_setup_logger_creates_logs_folder():
    """Тест: создаётся папка logs"""
    # Закрываем все хендлеры логгеров
    for logger_name in ['test_module', 'test_module2', 'test_module3', 'test_module4']:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
    
    # Небольшая пауза для закрытия файлов
    time.sleep(0.1)
    
    # Удаляем папку если есть
    if os.path.exists('logs'):
        import shutil
        shutil.rmtree('logs', ignore_errors=True)
    
    time.sleep(0.1)
    
    logger = setup_logger('test_module')
    
    assert os.path.exists('logs')
    assert os.path.exists('logs/test_module.log')

def test_setup_logger_returns_logger():
    """Тест: возвращается объект логгера"""
    logger = setup_logger('test_module2')
    assert isinstance(logger, logging.Logger)

def test_setup_logger_writes_logs():
    """Тест: логгер пишет в файл"""
    logger = setup_logger('test_module3')
    logger.info("Тестовое сообщение")
    
    with open('logs/test_module3.log', 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Тестовое сообщение" in content

def test_setup_logger_clears_old_handlers():
    """Тест: очищаются старые обработчики"""
    logger1 = setup_logger('test_module4')
    initial_count = len(logger1.handlers)
    
    logger2 = setup_logger('test_module4')
    # Должен быть 1 обработчик (старые удалились)
    assert len(logger2.handlers) <= 1
