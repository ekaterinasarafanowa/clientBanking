from typing import Any

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def test_mask_card_number_value() -> int:
    """Возвращает заранее заданный корректный 16-значный номер карты"""
    return 6578936740927385


def test_get_mask_card_number_from_fixture(test_mask_card_number_value: int) -> None:
    """Проверка работы функции с числом"""
    result = get_mask_card_number(test_mask_card_number_value)
    card_str = str(test_mask_card_number_value)
    assert result[:4] == card_str[:4]
    assert result[-4:] == card_str[-4:]
    assert "** ****" in result


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567812345678, "1234 56** **** 5678"),
        (1234567812345678, "1234 56** **** 5678"),
        (1000111122223333, "1000 11** **** 3333"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_get_mask_card_number(card_number: int, expected: str) -> None:
    """Проверка работы функции с граничными случаями"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number",
    [
        "",
        1234,  # слишком короткий
        12345678901234567890,  # слишком длинный
        "23456345678987654323478",
        123456781234567,  # 15 цифр
    ],
)
def test_get_mask_card_number_error(card_number: Any) -> None:
    """Проверка работы функции при неправильных входных параметрах"""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


def test_get_mask_card_number_none() -> None:
    """Проверка работы функции при передаче значения None"""
    with pytest.raises(ValueError):
        get_mask_card_number(None)  # type: ignore[arg-type]


@pytest.fixture
def test_get_mask_account_value() -> int:
    """Возвращает заранее заданный корректный номер счета"""
    return 73654108430135874305


def test_get_mask_account_fixture(test_get_mask_account_value: int) -> None:
    """Проверка работы функции правильности маскирования номера счета"""
    result = get_mask_account(test_get_mask_account_value)
    account_str = str(test_get_mask_account_value)
    assert result[-4:0] == account_str[-4:0]
    assert "**" in result


@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        (12345678, "**5678"),
        (123456789012, "**9012"),
        (10001234, "**1234"),
        (9876, "**9876"),
    ],
)
def test_get_mask_account(account_number: int, expected_mask: str) -> None:
    """Проверка работы функции с различными длинами"""
    assert get_mask_account(account_number) == expected_mask


@pytest.mark.parametrize(
    "raw_account",
    [
        ("123"),
        ("12a456"),
        (-123456),
        ("    "),
        ("12 3 "),
        ("*7651234"),
        78,
    ],
)
def test_get_mask_account_invalid(raw_account: int) -> None:
    """Проверка работы функции с различными форматами"""
    with pytest.raises(ValueError):
        get_mask_account(raw_account)
