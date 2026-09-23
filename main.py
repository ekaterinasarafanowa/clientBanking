from src.config import JSON_FILE, CSV_FILE, XLSX_FILE
from src.finance_reader import reader_finance_from_csv, reader_finance_from_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import get_financial_transactions
from src.widget import get_date, mask_account_card


def main():
    """Запускающая функция"""
    while True:
        print(
            "Привет! Добро пожаловать в программу работы с банковскими транзакциями."
            "\nВыберите необходимый пункт меню:"
            "\n1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла"
            "\n3. Получить информацию о транзакциях из XLSX-файла"
        )
        user_choice = input("Введите номер пункта меню:").strip()
        if user_choice == "1":
            data = get_financial_transactions(JSON_FILE)
            break
        elif user_choice == "2":
            data = reader_finance_from_csv(CSV_FILE)
            prepare_csv_like_data(data)
            break
        elif user_choice == "3":
            data = reader_finance_from_excel(XLSX_FILE)
            prepare_csv_like_data(data)
            break
        else:
            print("Неверный выбор. Попробуйте еще.")

    # Фильтр по статусу
    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        if status in ("EXECUTED", "CANCELED", "PENDING"):
            print(f"Операции отфильтрованы по статусу {status}")
            break
        else:
            print(f"Статус операции '{status}' недоступен.")

    filtered_data = filter_by_state(data, status)

    # Сортировка по дате
    while True:
        sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
        if sort_choice in ("да", "нет"):
            break
        print("Неверный ввод. Введите 'Да' или 'Нет'.")

    filtered_data_by_date = filtered_data
    if sort_choice == "да":
        while True:
            asc_desc = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
            if asc_desc in ("по возрастанию", "по убыванию"):
                filtered_data_by_date = sort_by_date(filtered_data, reverse=(asc_desc == "по убыванию"))
                break
            print("Неверный выбор. Введите 'по возрастанию' или 'по убыванию'.")

    # Фильтр по валюте
    while True:
        rub_choice = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
        if rub_choice in ("да", "нет"):
            break
        print("Неверный ввод. Введите 'Да' или 'Нет'.")

    filtered_data_by_rubles = filtered_data_by_date
    if rub_choice == "да":
        safe_data = [
            t
            for t in filtered_data_by_date
            if isinstance(t.get("operationAmount"), dict)
            and isinstance(t["operationAmount"].get("currency"), dict)
            and "code" in t["operationAmount"]["currency"]
        ]
        filtered_data_by_rubles = list(filter_by_currency(safe_data, "RUB"))

    # Фильтр по словам
    while True:
        search_choice = (
            input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
        )
        if search_choice in ("да", "нет"):
            break
        print("Неверный ввод. Введите 'Да' или 'Нет'.")

    filtered_data_by_search_operations = filtered_data_by_rubles
    if search_choice == "да":
        search_words = input("Введите слова для поиска в описании через пробел: ").strip()
        filtered_data_by_search_operations = process_bank_search(filtered_data_by_rubles, search_words)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not filtered_data_by_search_operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data_by_search_operations)}\n")
        for op in filtered_data_by_search_operations:
            date_str = get_date(op["date"])
            description = op.get("description", "")

            try:
                from_info = mask_account_card(str(op.get("from")).strip()) if op.get("from") else ""
            except (ValueError, TypeError, AttributeError):
                from_info = op.get("from") or ""

            try:
                to_info = mask_account_card(str(op.get("to")).strip()) if op.get("to") else ""
            except (ValueError, TypeError, AttributeError):
                to_info = op.get("to") or ""

            amount = op["operationAmount"]["amount"]
            currency = op["operationAmount"]["currency"]["code"]

            print(f"{date_str} {description}")
            if from_info and to_info:
                print(f"{from_info} -> {to_info}")
            elif to_info:
                print(f"{to_info}")
            elif from_info:
                print(f"{from_info}")
            print(f"Сумма: {amount} {currency}\n")


def prepare_csv_like_data(transactions: list[dict]) -> None:
    """Преобразует записи CSV/XLSX в структуру, аналогичную JSON."""
    for t in transactions:
        if "operationAmount" not in t:  # чтобы не перезаписывать, если уже есть
            t["operationAmount"] = {
                "amount": t.get("amount"),
                "currency": {"name": t.get("currency_name"), "code": t.get("currency_code")},
            }


if __name__ == "__main__":
    main()
