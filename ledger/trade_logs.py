import json
import requests
from datetime import datetime
from pathlib import Path
from connect_ib import connect_ib
from zoneinfo import ZoneInfo
import secret

# --- Telegram Config ---
TELEGRAM_BOT_TOKEN = secret.telegram_token  # Replace with your bot token
TELEGRAM_CHAT_ID = secret.chat_id  # Replace with your chat_id


def send_telegram(message):
    """Send message to Telegram with error handling"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",  # Enable markdown formatting
            },
            timeout=10,
        )
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


# --- IB Connection ---
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
            self.log_file.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create ledger dir if needed
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


def format_telegram_message(summary):
    """Format trade summary for Telegram with markdown"""
    side_emoji = "🟢" if summary["side"] == "BOT" else "🔴"
    pnl = summary["realizedPNL"]
    pnl_emoji = "💰" if pnl > 0 else "📉" if pnl < 0 else "➖"

    message = f"""
{side_emoji} *{summary['side']}* {summary['shares']} *{summary['symbol']}*
📊 Price: `${summary['price']:.2f}`
💵 Avg Price: `${summary['avgPrice']:.2f}`
💸 Commission: `${summary['commission']:.2f}`
{pnl_emoji} PnL: `${pnl:.2f}`
🕐 {summary['time']}
"""
    return message.strip()


if __name__ == "__main__":
    # Send startup notification
    send_telegram("🤖 *Trade Logger Started*\nMonitoring for new fills...")

    logger = TradeLogger("ledger/daily_log.json")

    for fill in fills:
        # Log the fill
        summary = logger.log_fill(fill)

        # Format and send to Telegram
        telegram_msg = format_telegram_message(summary)
        send_telegram(telegram_msg)

        # Also print to console
        print(f"Logged and sent: {summary['symbol']} {summary['side']}")
