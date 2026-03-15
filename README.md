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

### Модуль generators (Новый!)
Функции-генераторы для эффективной работы с большими объемами данных:

#### filter_by_currency
Фильтрует транзакции по заданной валюте и возвращает итератор.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
# Результат: первые две транзакции в USD
transaction_descriptions
Возвращает описания транзакций по очереди.

python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
# Результат: 
# Перевод организации
# Перевод со счета на счет
# Перевод со счета на счет
# Перевод с карты на карту
# Перевод организации
card_number_generator
Генерирует номера банковских карт в заданном диапазоне.

python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
# Результат:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005