from typing import Union
from src.logger_config import setup_logger

# астраиваем логгер для модуля masks
logger = setup_logger('masks')

def get_mask_card_number(card_number: Union[str, int]) -> str:
    """аскирует номер карты (показывает первые 6 и последние 4 цифры)"""
    try:
        card_str = str(card_number)
        logger.debug(f"аскирование карты: входные данные {card_str[:4]}...")
        
        if len(card_str) != 16:
            logger.error(f"еверная длина номера карты: {len(card_str)}")
            return "еверный номер карты"
        
        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"арта успешно замаскирована: {masked}")
        return masked
    except Exception as e:
        logger.error(f"шибка при маскировании карты: {e}")
        return "шибка"

def get_mask_account(account_number: Union[str, int]) -> str:
    """аскирует номер счета (показывает только последние 4 цифры)"""
    try:
        account_str = str(account_number)
        logger.debug(f"аскирование счета: входные данные ...{account_str[-4:]}")
        
        if len(account_str) < 4:
            logger.error(f"Слишком короткий номер счета: {len(account_str)}")
            return "еверный номер счета"
        
        masked = f"**{account_str[-4:]}"
        logger.info(f"Счет успешно замаскирован: {masked}")
        return masked
    except Exception as e:
        logger.error(f"шибка при маскировании счета: {e}")
        return "шибка"
