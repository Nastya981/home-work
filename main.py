from typing import List, Dict, Any, Optional
from src.utils import load_transactions_from_file
from src.external_api import convert_to_rubles
from src.search_filters import filter_by_state, search_transactions_by_description, filter_by_currency
from src.logger_config import setup_logger
from src.masks import get_mask_card_number, get_mask_account
import re

# Настраиваем логгер
logger = setup_logger('main')


def get_valid_status() -> str:
    """Запрашивает у пользователя корректный статус операции"""
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            logger.info(f"Пользователь выбрал статус: {status}")
            return status
        else:
            print(f"Статус операции \"{status}\" недоступен.")
            logger.warning(f"Пользователь ввел некорректный статус: {status}")


def get_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет"""
    while True:
        answer = input(f"{prompt} (Да/Нет): ").strip().lower()
        if answer in ['да', 'yes', 'y', 'д']:
            logger.info(f"Пользователь ответил Да на вопрос: {prompt}")
            return True
        elif answer in ['нет', 'no', 'n', 'н']:
            logger.info(f"Пользователь ответил Нет на вопрос: {prompt}")
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def get_sort_order() -> str:
    """Запрашивает направление сортировки"""
    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ['по возрастанию', 'возрастанию', 'asc', 'возраст']:
            return 'asc'
        elif order in ['по убыванию', 'убыванию', 'desc', 'убыв']:
            return 'desc'
        else:
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль"""
    try:
        # Получаем дату
        date_str = transaction.get('date', '')
        if 'T' in date_str:
            date_part = date_str.split('T')[0]
            year, month, day = date_part.split('-')
            formatted_date = f"{day}.{month}.{year}"
        else:
            formatted_date = date_str[:10] if len(date_str) >= 10 else date_str

        # Получаем описание
        description = transaction.get('description', 'Нет описания')

        # Получаем сумму и валюту
        operation_amount = transaction.get('operationAmount', {})
        amount = operation_amount.get('amount', '0')
        currency = operation_amount.get('currency', {}).get('code', 'RUB')

        # Конвертируем в рубли если нужно
        if currency != 'RUB':
            try:
                amount_float = convert_to_rubles(transaction)
                amount = f"{amount_float:.2f}"
                currency = 'RUB'
            except:
                pass

        # Форматируем from и to
        from_info = transaction.get('from', '')
        to_info = transaction.get('to', '')

        # Маскируем номера карт/счетов
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

        # Собираем строку
        result = f"\n{formatted_date} {description}"
        if from_info and to_info:
            result += f"\n{from_info} -> {to_info}"
        result += f"\nСумма: {amount} {currency}"

        return result

    except Exception as e:
        logger.error(f"Ошибка форматирования транзакции: {e}")
        return f"Ошибка форматирования: {transaction}"


def main() -> None:
    """Основная функция программы"""
    logger.info("=" * 50)
    logger.info("ЗАПУСК ПРОГРАММЫ")
    logger.info("=" * 50)

    print("\nПривет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ").strip()

    file_path = None
    if choice == '1':
        file_path = 'data/operations.json'
        print("\nДля обработки выбран JSON-файл.")
    elif choice == '2':
        file_path = 'data/transactions.csv'
        print("\nДля обработки выбран CSV-файл.")
    elif choice == '3':
        file_path = 'data/transactions_excel.xlsx'
        print("\nДля обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Используем JSON-файл по умолчанию.")
        file_path = 'data/operations.json'

    logger.info(f"Загрузка транзакций из файла: {file_path}")
    transactions = load_transactions_from_file(file_path)

    if not transactions:
        print("\nНе удалось загрузить транзакции. Проверьте наличие файла.")
        logger.error("Не удалось загрузить транзакции")
        return

    print(f"\nЗагружено {len(transactions)} транзакций.")

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_transactions = filter_by_state(transactions, status)
    print(f"\nОперации отфильтрованы по статусу \"{status}\"")
    logger.info(f"После фильтрации по статусу осталось {len(filtered_transactions)} транзакций")

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате?"):
        order = get_sort_order()
        reverse = (order == 'desc')
        filtered_transactions.sort(
            key=lambda x: x.get('date', ''),
            reverse=reverse
        )
        print(f"Операции отсортированы по дате {'по убыванию' if reverse else 'по возрастанию'}")

    # Фильтрация по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции?"):
        filtered_transactions = filter_by_currency(filtered_transactions, 'RUB')
        print(f"Отфильтровано {len(filtered_transactions)} рублевых транзакций")

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Поиск по слову в описании
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_transactions = search_transactions_by_description(filtered_transactions, search_word)
            print(f"Найдено {len(filtered_transactions)} транзакций, содержащих '{search_word}'")

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        print(format_transaction(transaction))

    logger.info(f"Программа завершена. Выведено {len(filtered_transactions)} транзакций")
    print("\n" + "=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    main()
