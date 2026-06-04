import re
from collections import Counter
from typing import List, Dict, Any
from src.utils import load_transactions_from_file
from src.external_api import convert_to_rubles
from src.logger_config import setup_logger
from src.masks import get_mask_card_number, get_mask_account
from src.process_operations import filter_operations_by_description, count_operations_by_categories

logger = setup_logger('main')


def filter_operations_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует операции по статусу"""
    status_upper = status.upper()
    return [t for t in transactions if t.get('state', '').upper() == status_upper]


def filter_operations_by_currency(transactions: List[Dict[str, Any]], currency: str = 'RUB') -> List[Dict[str, Any]]:
    """Фильтрует операции по валюте"""
    currency_upper = currency.upper()
    result = []
    for t in transactions:
        op_amount = t.get('operationAmount', {})
        t_currency = op_amount.get('currency', {}).get('code', '')
        if t_currency.upper() == currency_upper:
            result.append(t)
    return result


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода"""
    try:
        date_str = transaction.get('date', '')
        if 'T' in date_str:
            date_part = date_str.split('T')[0]
            year, month, day = date_part.split('-')
            formatted_date = f"{day}.{month}.{year}"
        else:
            formatted_date = date_str[:10] if len(date_str) >= 10 else date_str

        description = transaction.get('description', 'Нет описания')
        op_amount = transaction.get('operationAmount', {})
        amount = op_amount.get('amount', '0')
        currency = op_amount.get('currency', {}).get('code', 'RUB')

        if currency != 'RUB':
            try:
                amount_float = convert_to_rubles(transaction)
                amount = f"{amount_float:.2f}"
                currency = 'RUB'
            except:
                pass

        from_info = transaction.get('from', '')
        to_info = transaction.get('to', '')

        if from_info:
            parts = from_info.split()
            if len(parts) > 1:
                number = parts[-1]
                if len(number) == 16:
                    masked = get_mask_card_number(number)
                    from_info = f"{' '.join(parts[:-1])} {masked}"
                elif len(number) >= 4:
                    masked = get_mask_account(number)
                    from_info = f"{' '.join(parts[:-1])} {masked}"

        if to_info:
            parts = to_info.split()
            if len(parts) > 1:
                number = parts[-1]
                if len(number) == 16:
                    masked = get_mask_card_number(number)
                    to_info = f"{' '.join(parts[:-1])} {masked}"
                elif len(number) >= 4:
                    masked = get_mask_account(number)
                    to_info = f"{' '.join(parts[:-1])} {masked}"

        result = f"\n{formatted_date} {description}"
        if from_info and to_info:
            result += f"\n{from_info} -> {to_info}"
        result += f"\nСумма: {amount} {currency}"
        return result
    except Exception as e:
        logger.error(f"Ошибка форматирования: {e}")
        return f"Ошибка: {transaction}"


def get_valid_status() -> str:
    """Запрашивает корректный статус операции"""
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Статус: ").strip().upper()
        if status in valid_statuses:
            logger.info(f"Выбран статус: {status}")
            return status
        print(f"Статус операции \"{status}\" недоступлен.")


def get_yes_no(prompt: str) -> bool:
    """Запрашивает ответ Да/Нет"""
    while True:
        answer = input(f"{prompt} (Да/Нет): ").strip().lower()
        if answer in ['да', 'yes', 'y', 'д']:
            return True
        if answer in ['нет', 'no', 'n', 'н']:
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'")


def get_sort_order() -> str:
    """Запрашивает направление сортировки"""
    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ['по возрастанию', 'возрастанию', 'asc']:
            return 'asc'
        if order in ['по убыванию', 'убыванию', 'desc']:
            return 'desc'
        print("Введите 'по возрастанию' или 'по убыванию'")


def main() -> None:
    """Основная функция программы"""
    logger.info("=" * 50)
    logger.info("ЗАПУСК ПРОГРАММЫ")

    print("\nПривет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ").strip()
    file_map = {'1': 'data/operations.json', '2': 'data/transactions.csv', '3': 'data/transactions_excel.xlsx'}
    file_path = file_map.get(choice, 'data/operations.json')
    print(f"\nДля обработки выбран файл: {file_path}")

    transactions = load_transactions_from_file(file_path)
    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    print(f"\nЗагружено {len(transactions)} транзакций.")

    # Фильтрация по статусу
    status = get_valid_status()
    filtered = filter_operations_by_status(transactions, status)
    print(f"\nОперации отфильтрованы по статусу \"{status}\"")
    print(f"Найдено {len(filtered)} операций.")

    if not filtered:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате?"):
        order = get_sort_order()
        reverse = (order == 'desc')
        filtered.sort(key=lambda x: x.get('date', ''), reverse=reverse)
        print(f"Операции отсортированы по дате {'по убыванию' if reverse else 'по возрастанию'}")

    # Фильтрация по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции?"):
        filtered = filter_operations_by_currency(filtered, 'RUB')
        print(f"Отфильтровано {len(filtered)} рублевых транзакций")

    # Поиск по слову в описании
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered = filter_operations_by_description(filtered, search_word)
            print(f"Найдено {len(filtered)} транзакций, содержащих '{search_word}'")

    if not filtered:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Пример подсчёта по категориям (демонстрация)
    categories = ['Перевод', 'Открытие', 'Оплата']
    category_counts = count_operations_by_categories(filtered, categories)
    print(f"\nПодсчёт по категориям: {category_counts}")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered)}")
    for transaction in filtered:
        print(format_transaction(transaction))

    logger.info("ПРОГРАММА ЗАВЕРШЕНА")
    print("\n" + "=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    main()
