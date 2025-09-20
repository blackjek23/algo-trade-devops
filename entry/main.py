# file: main.py
import config
from tickers import load_tickers
from data_fetch import get_historical_data
from entry_check import run_entry_check
from entry_orders import place_entry_orders
from positions import get_open_tickers

MAX_POSITIONS = 50  # maximum number of holdings allowed


def main():

    tickers = load_tickers("stocks.txt")
    if not tickers:
        return

    # Fetch open positions first
    open_positions = get_open_tickers()
    held_symbols = set(open_positions.keys())

    # Check portfolio size limit
    if len(held_symbols) >= MAX_POSITIONS:
        return

    for symbol in tickers:

        # Skip if already holding this stock
        if symbol in held_symbols:
            continue

        # Check if adding one more would exceed max positions
        if len(held_symbols) >= MAX_POSITIONS:
            break

        # 1. Download stock data (just this symbol)
        hist_data = get_historical_data(
            [symbol], period=config.YF_PERIOD, interval=config.YF_INTERVAL
        )

        if symbol not in hist_data or hist_data[symbol].empty:
            continue

        # 2. Check entry signal
        signals = run_entry_check({symbol: hist_data[symbol]})

        if not signals:
            continue

        # 3. Place order immediately
        place_entry_orders(signals, allocation_pct=0.02)
        # 2% allocation per new position


if __name__ == "__main__":
    main()
