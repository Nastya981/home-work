"""Интеграционные тесты для проверки взаимодействия функций."""

import pytest
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия функций."""

    def test_full_processing_flow(self, sample_transactions):
        """Тестирование полного цикла обработки данных."""
        executed = filter_by_state(sample_transactions, "EXECUTED")
        sorted_executed = sort_by_date(executed)
        assert len(sorted_executed) == 5
        assert sorted_executed[0]["date"] > sorted_executed[-1]["date"]

    @pytest.mark.parametrize(
        "card_info, expected_mask",
        [
            ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
            ("Счет 73654108430135874305", "**4305"),
        ],
    )
    def test_mask_functions_integration(self, card_info, expected_mask):
        """Проверка интеграции функций маскировки."""
        parts = card_info.split()
        number = parts[-1]
        if "Счет" in card_info:
            result = get_mask_account(number)
        else:
            result = get_mask_card_number(number)
        assert result == expected_mask

    def test_date_conversion_and_filtering(self, sample_transactions):
        """Проверка преобразования даты и фильтрации."""
        for transaction in sample_transactions:
            if "date" in transaction:
                formatted_date = get_date(transaction["date"])
                transaction["formatted_date"] = formatted_date
        for transaction in sample_transactions:
            if "date" in transaction:
                assert len(transaction["formatted_date"]) == 10
                assert transaction["formatted_date"].count(".") == 2

    def test_mask_account_card_with_filtering(self, sample_card_account_data):
        """Проверка совместной работы mask_account_card и фильтрации."""
        for item in sample_card_account_data:
            masked = mask_account_card(item)
            assert isinstance(masked, str)
            if "Счет" in item:
                assert "**" in masked
            else:
                assert "****" in masked or "**" in masked
