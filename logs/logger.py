import os
import json
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

PORTFOLIO_LOG = os.path.join(LOGS_DIR, "portfolio_state.json")


# Portfolio state logging (JSON per line)
def log_portfolio_state(holdings, summary):
    """
    holdings: list of dicts, each with keys: symbol, position_size, pnl
    summary: dict with keys: position_amount, sum_pnl, free_cash, portfolio_value
    """
    if os.path.exists(PORTFOLIO_LOG) and os.path.getsize(PORTFOLIO_LOG) > 0:
        with open(PORTFOLIO_LOG, "r") as f:
            logs = json.load(f)
    else:
        logs = []  # Create new log list if empty or missing
    log_entry = {
        "date": datetime.now().date().isoformat(),
        "holdings": holdings,
        "summary": summary,
    }
    logs.append(log_entry)

    with open(PORTFOLIO_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
