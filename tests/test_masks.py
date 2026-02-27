import unittest

from src.masks import get_mask_account, get_mask_card_number


class TestMasks(unittest.TestCase):

    def test_get_mask_card_number(self):
        # Тест с корректным номером карты
        self.assertEqual(get_mask_card_number("7000792289606361"), "7000 79** **** 6361")
        # Тест с номером, содержащим пробелы и спецсимволы
        self.assertEqual(get_mask_card_number("7000 7922-8960-6361"), "7000 79** **** 6361")

    def test_get_mask_account(self):
        # Тест с корректным номером счёта
        self.assertEqual(get_mask_account("73654108430135874305"), "**4305")
        # Тест с номером, содержащим пробелы
        self.assertEqual(get_mask_account("7365 4108 4301 3587 4305"), "**4305")

    def test_invalid_card_number(self):
        with self.assertRaises(ValueError):
            get_mask_card_number("1234")  # Слишком короткий номер

    def test_invalid_account_number(self):
        with self.assertRaises(ValueError):
            get_mask_account("123")  # Слишком короткий номер счёта


if __name__ == "__main__":
    unittest.main()
