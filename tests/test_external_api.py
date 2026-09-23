import unittest
from unittest.mock import MagicMock, patch

from src.external_api import transaction_amount_in_rubles  # Замените your_module на имя вашего модуля


class TestTransactionAmountInRubles(unittest.TestCase):
    @patch("requests.get")
    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_key", "BASE_URL": "http://test.url"})
    def test_rub_conversion(self, mock_get):
        """Тест для транзакции в рублях (конверсия не требуется)"""
        transaction = {"amount": "100.50", "currency": "RUB"}
        result = transaction_amount_in_rubles(transaction)
        self.assertEqual(result, 100.50)
        mock_get.assert_not_called()

    @patch("requests.get")
    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_key", "BASE_URL": "http://test.url"})
    def test_usd_conversion_success(self, mock_get):
        """Тест успешной конверсии USD в RUB"""
        # Настраиваем mock ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}  # Исправленная структура ответа
        mock_get.return_value = mock_response

        transaction = {"amount": "10.00", "currency": "USD"}
        result = transaction_amount_in_rubles(transaction)

        self.assertEqual(result, 755.00)  # 10.00 * 75.5 = 755.00
        mock_get.assert_called_once_with(
            "http://test.url", headers={"apikey": "test_key"}, params={"from": "USD", "to": "RUB", "amount": 10.00}
        )

    @patch("requests.get")
    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_key", "BASE_URL": "http://test.url"})
    def test_invalid_amount(self, mock_get):
        """Тест обработки невалидной суммы"""
        transaction = {"amount": "invalid", "currency": "USD"}

        with self.assertRaises(ValueError):
            transaction_amount_in_rubles(transaction)

        mock_get.assert_not_called()
