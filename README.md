# Проект по маскировке банковских карт и счетов

## Описание проекта
Данный проект представляет собой набор функций для маскировки номеров банковских карт и счетов, а также для обработки и фильтрации списка транзакций. Проект разработан на Python и включает в себя модули для различных операций с банковскими данными.

## Модули проекта

### Модуль masks
Функции для маскировки номеров карт и счетов:
- `get_mask_card_number(card_number: str) -> str` - маскирует номер карты (пример: 7000 79** **** 6361)
- `get_mask_account(account_number: str) -> str` - маскирует номер счета (пример: **4305)

### Модуль widget
Функции для работы с виджетами:
- `mask_account_card(account_card: str) -> str` - маскирует карту или счет в зависимости от типа
- `get_date(date_string: str) -> str` - преобразует дату из ISO формата в формат ДД.ММ.ГГГГ

### Модуль processing
Функции для обработки списков транзакций:
- `filter_by_state(transactions: list, state: str = "EXECUTED") -> list` - фильтрует транзакции по статусу
- `sort_by_date(transactions: list, reverse: bool = True) -> list` - сортирует транзакции по дате

### Модуль generators
Функции-генераторы для эффективной работы с большими объемами данных:
- `filter_by_currency(transactions, currency)` - фильтрует транзакции по валюте
- `transaction_descriptions(transactions)` - возвращает описания транзакций
- `card_number_generator(start, end)` - генерирует номера карт в заданном диапазоне

### Модуль decorators (Новый!)
Декораторы для логирования и отладки:

#### Декоратор log
Автоматически логирует начало и конец выполнения функции, а также результаты или возникшие ошибки.

```python
from src.decorators import log

# Логирование в консоль
@log()
def my_function(x, y):
    return x + y

# Логирование в файл
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

# Пример успешного выполнения (в лог-файл запишется: "my_function ok")
my_function(1, 2)

# Пример с ошибкой (в лог-файл запишется: "my_function error: ZeroDivisionError. Inputs: (1, 0), {}")
my_function(1, 0)