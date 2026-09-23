from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR = BASE_DIR / "data"
JSON_FILE = DATA_DIR / "operations.json"
CSV_FILE = DATA_DIR / "transactions.csv"
XLSX_FILE = DATA_DIR / "transactions_excel.xlsx"
