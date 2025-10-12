import csv
from datetime import datetime

LOGS_DIR = "/logs"
EXIT_LOG = f"{LOGS_DIR}/exit_actions.csv"


def log_exit_order(date_str=None, ticker=None, order_type=None, qty=None):
    """
    Log exit order to logs/exit_actions.csv
    Columns: date, ticker, order_type, qty
    """
    if date_str is None:
        date_str = datetime.now().date().isoformat()
    file_exists = False
    try:
        with open(EXIT_LOG, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass
    with open(EXIT_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "ticker", "order_type", "qty"])
        writer.writerow([date_str, ticker, order_type, qty])
