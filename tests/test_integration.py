"""
Интеграционные тесты для проверки взаимодействия функций
"""
import pytest
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.masks import get_mask_card_number, get_mask_account


class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия функций"""

    def test_full_processing_flow(self, sample_transactions):
        """Тестирование полного цикла обработки данных"""
        # Фильтруем только выполненные транзакции
        executed = filter_by_state(sample_transactions, "EXECUTED")

        # Сортируем по дате
        sorted_executed = sort_by_date(executed)

        # Проверяем результат - в sample_transactions из conftest.py 5 транзакций со статусом EXECUTED
        assert len(sorted_executed) == 5
        # Проверяем, что сортировка по убыванию работает
        for i in range(len(sorted_executed) - 1):
            assert sorted_executed[i]["date"] >= sorted_executed[i + 1]["date"]

    @pytest.mark.parametrize("card_info, expected_mask", [
        ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
        ("Счет 73654108430135874305", "**4305"),
    ])
    def test_mask_functions_integration(self, card_info, expected_mask):
        """Проверка интеграции функций маскировки"""
        # Получаем номер из строки
        parts = card_info.split()
        number = parts[-1]

        if "Счет" in card_info:
            result = get_mask_account(number)
        else:
            result = get_mask_card_number(number)

        assert result == expected_mask

    def test_date_conversion_and_filtering(self, sample_transactions):
        """Проверка преобразования даты и фильтрации"""
        # Преобразуем даты для всех транзакций
        for transaction in sample_transactions:
            if "date" in transaction:
                formatted_date = get_date(transaction["date"])
                transaction["formatted_date"] = formatted_date

        # Проверяем, что форматирование прошло успешно
        for transaction in sample_transactions:
            if "date" in transaction:
                assert len(transaction["formatted_date"]) == 10
                assert transaction["formatted_date"].count(".") == 2
                # Проверяем, что формат соответствует ДД.ММ.ГГГГ
                day, month, year = transaction["formatted_date"].split(".")
                assert len(day) == 2
                assert len(month) == 2
                assert len(year) == 4
                assert day.isdigit()
                assert month.isdigit()
                assert year.isdigit()

    def test_filter_and_sort_combined(self, sample_transactions):
        """Тестирование комбинации фильтрации и сортировки"""
        # Фильтруем по разным статусам и проверяем сортировку
        for state in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered = filter_by_state(sample_transactions, state)
            sorted_filtered = sort_by_date(filtered)

            # Проверяем, что все элементы имеют правильный статус
            if filtered:
                assert all(item["state"] == state for item in filtered)
                # Проверяем сортировку
                for i in range(len(sorted_filtered) - 1):
                    assert sorted_filtered[i]["date"] >= sorted_filtered[i + 1]["date"]