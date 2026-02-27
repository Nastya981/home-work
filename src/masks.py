def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты в формате XXXX XX** **** XXXX."""
    # Убираем все нечисловые символы
    cleaned = "".join(char for char in card_number if char.isdigit())
    # Проверяем длину номера
    if len(cleaned) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")
    # Формируем маску
    masked = f"{cleaned[0:4]} " f"{cleaned[4:6]}** " f"**** " f"{cleaned[12:16]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счёта в формате **XXXX."""
    # Убираем все нечисловые символы
    cleaned = "".join(char for char in account_number if char.isdigit())
    # Формируем маску: оставляем последние 4 цифры, остальные заменяем на **
    if len(cleaned) < 4:
        raise ValueError("Номер счёта должен быть длиннее 4 цифр.")
    masked = f"**{cleaned[-4:]}"
    return masked
