"""
Модуль для работы с виджетами банковских операций.
"""


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер счета или карты.

    Параметры:
        account_info: строка с типом и номером счета/карты

    Возвращает:
        строку с замаскированным номером
    """
    parts = account_info.rsplit(' ', 1)
    if len(parts) != 2:
        return account_info

    account_type = parts[0]
    number = parts[1]

    if len(number) == 16:  # карта
        masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    else:  # счет
        masked = f"**{number[-4:]}"

    return f"{account_type} {masked}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Параметры:
        date_str: строка с датой в формате "YYYY-MM-DDTHH:MM:SS.mmmmmm"

    Возвращает:
        строку с датой в формате "ДД.ММ.ГГГГ"
    """
    if not date_str:
        return ""

    date_part = date_str.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"
