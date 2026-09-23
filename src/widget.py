from .masks import get_mask_account, get_mask_card_number


def mask_account_card(str_account: str) -> str:
    """Функция обрабатывает информацию как о картах, так и о счетах"""
    account_details = str_account.split(" ")
    for detail in account_details:
        if detail.lower().startswith("счет"):
            digit_part = next((d for d in account_details if d.isdigit()))
            return f"Счет {get_mask_account(int(digit_part))}"
    for detail in account_details:
        if detail.isdigit():
            card_name = " ".join([part for part in account_details if not part.isdigit()])
            return f"{card_name} {get_mask_card_number(int(detail))}"
    return "Ошибка: неверный формат данных"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата 'ГГГГ-ММ-ДДT...' в 'ДД.ММ.ГГГГ'."""
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
