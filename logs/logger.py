import os
import csv
import json
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

PORTFOLIO_LOG = os.path.join(LOGS_DIR, "portfolio_state.json")
EXIT_LOG = os.path.join(LOGS_DIR, "exit_actions.csv")
ENTRY_LOG = os.path.join(LOGS_DIR, "entry_actions.csv")


# Portfolio state logging (JSON per line)
def log_portfolio_state(holdings, summary):
    """
    holdings: list of dicts, each with keys: symbol, position_size, pnl
    summary: dict with keys: position_amount, sum_pnl, free_cash, portfolio_value
    """
    with open(PORTFOLIO_LOG, "a") as f:
        log_entry = {
            "date": datetime.now().date().isoformat(),
            "holdings": holdings,
            "summary": summary,
        }
        f.write(json.dumps(log_entry) + "\n")
