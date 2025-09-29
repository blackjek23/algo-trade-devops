import json
from datetime import datetime
from pathlib import Path
from connect_ib import connect_ib
from zoneinfo import ZoneInfo

ib = connect_ib()
fills = ib.fills()


# --- summary extraction ---
def summarize_fill(fill):
    utc_time = fill.execution.time
    local_time = utc_time.astimezone(ZoneInfo("Asia/Jerusalem"))
    readable_time = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return {
        "time": readable_time,
        "symbol": fill.contract.symbol,
        "side": fill.execution.side,
        "shares": fill.execution.shares,
        "price": fill.execution.price,
        "avgPrice": fill.execution.avgPrice,
        "commission": fill.commissionReport.commission,
        "realizedPNL": fill.commissionReport.realizedPNL,
    }


# --- logger ---
class TradeLogger:
    def __init__(self, log_file="ledger/daily_log.json"):
        self.log_file = Path(log_file)
        if not self.log_file.exists():
            self.log_file.write_text("[]")  # initialize with empty list

    def log_fill(self, fill):
        summary = summarize_fill(fill)

        # safely load JSON
        try:
            text = self.log_file.read_text().strip()
            data = json.loads(text) if text else []  # handle empty file
        except json.JSONDecodeError:
            data = []  # fallback if corrupted

        # append new entry
        data.append(summary)

        # save back
        self.log_file.write_text(json.dumps(data, indent=2))

        return summary


if __name__ == "__main__":
    for fill in fills:
        logger = TradeLogger("ledger/daily_log.json")
        # when a fill arrives
        summary = logger.log_fill(fill)
        telegram_msg = (
            f"{summary['time']} | {summary['side']} {summary['shares']} {summary['symbol']} "
            f"@ {summary['price']} | Comm: {summary['commission']} | PnL: {summary['realizedPNL']}"
        )
        # send telegram_msg with your bot
        print(telegram_msg)
