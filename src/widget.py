def mask_account_info(account_str):
    """
    Маскирует номер карты или счёта.
    Для карт: оставляет видимыми только последние 4 цифры, остальные заменяет на '*'.
    Для счетов: оставляет видимыми только последние 4 цифры, остальные заменяет на '*'.

    Аргументы:
        account_str (str): Строка с типом и номером (например, 'Visa Platinum 7000792289606361').

    Возвращает:
        str: Маскированная строка.
    """
    # Разделяем строку на части
    parts = account_str.split()
    number = parts[-1]  # Номер — последний элемент
    account_type = ' '.join(parts[:-1])  # Тип — все элементы, кроме последнего

    # Очищаем номер от нечисловых символов
    clean_number = ''.join(char for char in number if char.isdigit())

    if not clean_number:
        raise ValueError("Номер не найден или некорректен")

    # Маскировка для карт (Visa, Maestro, MasterCard, Visa Classic, Visa Platinum, Visa Gold)
    if any(card_type in account_type for card_type in ['Visa', 'Maestro', 'MasterCard']):
        masked_part = '*' * (len(clean_number) - 4)
        visible_part = clean_number[-4:]
        masked_number = f"{masked_part} {visible_part}"
        return f"{account_type} {masked_number}"

    # Маскировка для счетов
    elif 'Счёт' in account_type:
        masked_part = '*' * (len(clean_number) - 4)
        visible_part = clean_number[-4:]
        masked_number = f"{masked_part}{visible_part}"
        return f"{account_type} {masked_number}"

    else:
        raise ValueError(f"Неизвестный тип аккаунта: {account_type}")


from datetime import datetime


def get_date(date_str):
    """
    Преобразует строку с датой в формате ISO (например, '2024-03-11T02:26:18.671407')
    в формат 'ДД.ММ.ГГГГ'.

    Аргументы:
        date_str (str): Строка с датой в ISO-формате.

    Возвращает:
        str: Дата в формате 'ДД.ММ.ГГГГ'.
    """
    # Обработка Z как +00:00 (если присутствует)
    if date_str.endswith('Z'):
        date_str = date_str.replace('Z', '+00:00')

    # Преобразуем строку в объект datetime
    dt = datetime.fromisoformat(date_str)

    # Форматируем дату
    return dt.strftime('%d.%m.%Y')
