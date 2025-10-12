import csv
from datetime import datetime

LOGS_DIR = "/logs"
ENTRY_LOG = f"{LOGS_DIR}/entry_actions.csv"


def log_entry_order(date_str=None, ticker=None, order_type=None, qty=None):
    """
    Log entry order to logs/entry_actions.csv
    Columns: date, ticker, order_type, qty
    """
    if date_str is None:
        date_str = datetime.now().date().isoformat()
    file_exists = False
    try:
        with open(ENTRY_LOG, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass
    with open(ENTRY_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "ticker", "order_type", "qty"])
        writer.writerow([date_str, ticker, order_type, qty])
