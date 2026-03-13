"""
Интеграционные тесты для проверки взаимодействия функций.
"""
import pytest
from src.processing import filter_by_state, sort_by_date
from src.masks import get_mask_card_number, get_mask_account


class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия функций."""

    def test_full_processing_flow(self, sample_transactions):
        """Тестирование полного цикла обработки данных."""
        # Фильтруем только выполненные транзакции
        executed = filter_by_state(sample_transactions, "EXECUTED")

        # Сортируем по дате
        sorted_executed = sort_by_date(executed)

        # Проверяем результат - должно быть 4 EXECUTED транзакции
        assert len(sorted_executed) == 4
        # Проверяем, что сортировка по убыванию работает
        for i in range(len(sorted_executed) - 1):
            assert sorted_executed[i]["date"] >= sorted_executed[i + 1]["date"]

    @pytest.mark.parametrize("card_info, expected_mask", [
        ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
        ("Счет 73654108430135874305", "**4305"),
    ])
    def test_mask_functions_integration(self, card_info, expected_mask):
        """Проверка интеграции функций маскировки."""
        parts = card_info.split()
        number = parts[-1]

        if "Счет" in card_info:
            result = get_mask_account(number)
        else:
            result = get_mask_card_number(number)

        assert result == expected_mask

