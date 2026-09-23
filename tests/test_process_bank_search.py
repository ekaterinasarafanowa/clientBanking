import pytest

from src.processing import process_bank_search


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


def test_process_bank_search(sample_data):
    """
    Проверяет, что функция process_bank_search корректно находит операции,
    содержащие ключевое слово "перевод" (без учёта регистра) в описании.
    """
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 2
    assert all("перевод" in op["description"].lower() for op in result)


def test_process_bank_search_empty_string_returns_all(sample_data):
    """
    Проверяет, что если в функцию передать пустую строку для поиска,
    то она возвращает все операции без фильтрации.
    """
    result = process_bank_search(sample_data, "")
    assert result == sample_data


def test_process_bank_search_no_matches(sample_data):
    """
    Проверяет, что если ни одна категория не встречается в описаниях,
    возвращается пустой список.
    """
    result = process_bank_search(sample_data, "Автомобиль")
    assert result == []
