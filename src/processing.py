import re
from collections import Counter


def filter_by_state(bank_operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_transactions = []

    for operation in bank_operations:
        if operation.get("state") == state:
            filtered_transactions.append(operation)

    return filtered_transactions


def sort_by_date(bank_operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по дате."""
    return sorted(bank_operations, key=lambda x: x["date"], reverse=reverse)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует список операций, оставляя только те, в описании которых есть указанная строка"""
    pattern = re.compile(search, re.IGNORECASE)
    if not search.strip():  # Проверка на пустую строку или пробелы
        return data
    filtered_operations = []
    for operation in data:
        if operation.get("description") and pattern.search(operation["description"]):
            filtered_operations.append(operation)
    return filtered_operations


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по категориям."""
    category_counts = Counter()
    categories_lower = [cat.lower() for cat in categories]
    for operation in data:
        description = operation.get("description")
        if isinstance(description, str):
            desc_lower = operation["description"].lower()
            for cat in categories_lower:
                if cat in desc_lower:
                    category_counts[cat] += 1

    return dict(category_counts)
