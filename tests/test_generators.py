"""Тесты для модуля generators."""

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тестирование фильтрации по USD."""
        result = list(filter_by_currency(sample_transactions, "USD"))
        assert len(result) == 3
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тестирование фильтрации по RUB."""
        result = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(result) == 2
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["code"] == "RUB"

    @pytest.mark.parametrize(
        "currency, expected_count",
        [
            ("USD", 3),
            ("RUB", 2),
            ("EUR", 0),
            ("GBP", 0),
        ],
    )
    def test_filter_by_currency_parametrized(self, sample_transactions, currency, expected_count):
        """Параметризованный тест для разных валют."""
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == expected_count

    def test_filter_by_currency_empty_list(self):
        """Тестирование с пустым списком."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_filter_by_currency_no_transactions(self):
        """Тестирование с None вместо списка."""
        with pytest.raises(TypeError):
            list(filter_by_currency(None, "USD"))

    def test_filter_by_currency_malformed_transactions(self):
        """Тестирование с некорректными транзакциями."""
        transactions = [
            {},  # пустой словарь
            {"id": 1},  # без operationAmount
            {"operationAmount": {}},  # без currency
            {"operationAmount": {"currency": {}}},  # без code
            {"operationAmount": {"currency": {"code": "USD"}}},  # корректная
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["operationAmount"]["currency"]["code"] == "USD"


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_transaction_descriptions(self, sample_transactions):
        """Тестирование получения описаний."""
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        result = list(transaction_descriptions(sample_transactions))
        assert result == expected_descriptions

    def test_transaction_descriptions_empty_list(self):
        """Тестирование с пустым списком."""
        result = list(transaction_descriptions([]))
        assert result == []

    def test_transaction_descriptions_missing_description(self):
        """Тестирование с отсутствующими описаниями."""
        transactions = [
            {"id": 1, "description": "Описание 1"},
            {"id": 2},  # без description
            {"id": 3, "description": ""},  # пустое описание
            {"id": 4, "description": "Описание 4"},
        ]
        expected = ["Описание 1", "Описание 4"]
        result = list(transaction_descriptions(transactions))
        assert result == expected

    def test_transaction_descriptions_generator_type(self, sample_transactions):
        """Проверка, что функция возвращает генератор."""
        result = transaction_descriptions(sample_transactions)
        from collections.abc import Generator

        assert isinstance(result, Generator)


class TestCardNumberGenerator:
    """Тесты для функции card_number_generator."""

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            (1, 1, ["0000 0000 0000 0001"]),
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (
                9999999999999995,
                9999999999999997,
                ["9999 9999 9999 9995", "9999 9999 9999 9996", "9999 9999 9999 9997"],
            ),
        ],
    )
    def test_card_number_generator_valid_range(self, start, end, expected):
        """Тестирование генерации номеров в корректном диапазоне."""
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_format(self):
        """Проверка форматирования номеров карт."""
        result = list(card_number_generator(1, 5))
        for card_number in result:
            assert len(card_number) == 19  # 16 цифр + 3 пробела
            assert card_number.count(" ") == 3
            parts = card_number.split()
            assert len(parts) == 4
            for part in parts:
                assert len(part) == 4
                assert part.isdigit()

    def test_card_number_generator_boundaries(self):
        """Тестирование граничных значений."""
        # Нижняя граница
        result = list(card_number_generator(0, 2))
        assert result[0] == "0000 0000 0000 0001"  # должно начаться с 1

        # Верхняя граница
        result = list(card_number_generator(9999999999999998, 10000000000000000))
        assert len(result) == 2
        assert result[-1] == "9999 9999 9999 9999"

    def test_card_number_generator_reverse_range(self):
        """Тестирование с обратным диапазоном (start > end)."""
        result = list(card_number_generator(5, 1))
        assert result == []  # должно вернуть пустой список

    def test_card_number_generator_generator_type(self):
        """Проверка, что функция возвращает генератор."""
        result = card_number_generator(1, 5)
        from collections.abc import Generator

        assert isinstance(result, Generator)
