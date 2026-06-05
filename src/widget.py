import re
from typing import Union


def mask_account_card(card_or_account: Union[str, int]) -> str:
    """
    Принимает строку с номером карты или счета и возвращает замаскированную версию
    """
    try:
        parts = str(card_or_account).split()
        if len(parts) < 2:
            return "Неверный формат"

        card_type = " ".join(parts[:-1])
        number = parts[-1]
        number_clean = re.sub(r'[\s\-]', '', number)

        if len(number_clean) == 16:
            masked_number = f"{number_clean[:4]} {number_clean[4:6]}** **** {number_clean[-4:]}"
            return f"{card_type} {masked_number}"
        elif len(number_clean) >= 4:
            masked_number = f"**{number_clean[-4:]}"
            return f"{card_type} {masked_number}"
        else:
            return "Неверный номер"
    except Exception:
        return "Ошибка обработки"


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой и возвращает в формате ДД.ММ.ГГГГ
    """
    try:
        if 'T' in date_string:
            date_part = date_string.split('T')[0]
            year, month, day = date_part.split('-')
            return f"{day}.{month}.{year}"
        return "Неверная дата"
    except Exception:
        return "Неверная дата"
