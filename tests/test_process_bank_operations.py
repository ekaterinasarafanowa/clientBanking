import pytest

from src.processing import process_bank_operations


@pytest.fixture
def sample_data():
    """Тестовые данные — список транзакций с разными описаниями."""
    return [
        {"description": "Перевод с карты на карту", "amount": 100},
        {"description": "Оплата услуг ЖКХ", "amount": 200},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Перевод организации", "amount": 400},
        {"description": None, "amount": 500},
    ]


def test_process_bank_operations_counts(sample_data):
    """
    Проверяет, что функция process_bank_operations корректно
    подсчитывает количество операций для каждой категории.
    """
    categories = ["перевод", "оплата", "покупка"]
    result = process_bank_operations(sample_data, categories)
    assert result == {"перевод": 2, "оплата": 1, "покупка": 1}


def test_process_bank_operations_no_matches(sample_data):
    """
    Проверяет, что если ни одна категория не встречается в описаниях,
    возвращается пустой словарь.
    """
    categories = ["автомобиль"]
    result = process_bank_operations(sample_data, categories)
    assert result == {}


def test_process_bank_operations_empty_categories(sample_data):
    result = process_bank_operations(sample_data, [])
    assert result == {}
