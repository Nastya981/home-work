"""Модуль для работы с виджетами."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Маскирует номер карты или счета."""
    parts = account_card.split()
    if "Счет" in account_card:
        return f"Счет {get_mask_account(parts[-1])}"
    else:
        card_number = parts[-1]
        card_type = " ".join(parts[:-1])
        return f"{card_type} {get_mask_card_number(card_number)}"


def get_date(date_string: str) -> str:
    """Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ."""
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
