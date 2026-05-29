from typing import Union
import logging
import os
import re

# Настраиваем логгер для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

# Создаём папку logs если её нет
os.makedirs('logs', exist_ok=True)

# Настраиваем file_handler - mode='a' для дозаписи
file_handler = logging.FileHandler('logs/masks.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настраиваем формат
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Маскирует номер карты (показывает первые 6 и последние 4 цифры)

    Пример: 1234567890123456 -> 1234 56** **** 3456
    """
    try:
        # Удаляем все пробелы и дефисы
        card_str = re.sub(r'[\s\-]', '', str(card_number))
        logger.debug(f"Начало маскирования карты: входные данные {card_str[:4]}...")

        # Проверяем длину номера карты
        if len(card_str) != 16:
            logger.error(f"Неверная длина номера карты: {len(card_str)}. Ожидается 16 цифр.")
            raise ValueError(f"Неверная длина номера карты: {len(card_str)}. Ожидается 16 цифр.")

        # Маскируем номер карты
        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"Успешно замаскирована карта: {masked}")
        return masked

    except ValueError as e:
        logger.error(f"Ошибка валидации карты: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при маскировании карты: {e}")
        raise ValueError(f"Ошибка при маскировании карты: {e}")


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Маскирует номер счета (показывает только последние 4 цифры)

    Пример: 12345678901234567890 -> **7890
    """
    try:
        account_str = str(account_number)
        logger.debug(f"Начало маскирования счета: ...{account_str[-4:]}")

        # Проверяем длину номера счета
        if len(account_str) < 4:
            logger.error(f"Слишком короткий номер счета: {len(account_str)} цифр. Минимум 4 цифры.")
            raise ValueError(f"Слишком короткий номер счета: {len(account_str)} цифр. Минимум 4 цифры.")

        # Маскируем номер счета
        masked = f"**{account_str[-4:]}"
        logger.info(f"Успешно замаскирован счет: {masked}")
        return masked

    except ValueError as e:
        logger.error(f"Ошибка валидации счета: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при маскировании счета: {e}")
        raise ValueError(f"Ошибка при маскировании счета: {e}")
