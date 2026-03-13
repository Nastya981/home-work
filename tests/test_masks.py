"""Модуль для маскировки номеров карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты в формате XXXX XX** **** XXXX."""
    # Убираем все нечисловые символы
    cleaned = "".join(char for char in card_number if char.isdigit())
    # Проверяем длину номера
    if len(cleaned) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")
    # Маскируем номер
    return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX."""
    # Убираем все нечисловые символы
    cleaned = "".join(char for char in account_number if char.isdigit())
    # Проверяем, что номер не пустой
    if not cleaned:
        raise ValueError("Номер счета не может быть пустым.")
    # Маскируем номер
    return f"**{cleaned[-4:]}"