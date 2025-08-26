# file: main.py
import config
from tickers import load_tickers
from data_fetch import get_historical_data
from entry_check import run_entry_check
from entry_orders import place_entry_orders
from positions import get_open_tickers

MAX_POSITIONS = 50  # maximum number of holdings allowed

def main():
    print("🚀 Starting Sequential Entry Bot")

    tickers = load_tickers("stocks.txt")
    if not tickers:
        print("⚠️ No tickers found, exiting.")
        return

    # Fetch open positions first
    open_positions = get_open_tickers()
    held_symbols = set(open_positions.keys())

    print(f"📋 {len(tickers)} tickers loaded. Processing one by one...")
    print(f"🔒 Currently holding: {', '.join(held_symbols) if held_symbols else 'None'}")

    # Check portfolio size limit
    if len(held_symbols) >= MAX_POSITIONS:
        print(f"🚫 Already at max positions ({MAX_POSITIONS}). No new entries allowed.")
        return

    for symbol in tickers:
        print(f"\n--- 🔍 Checking {symbol} ---")

        # Skip if already holding this stock
        if symbol in held_symbols:
            print(f"⏭️ Already holding {symbol}, skipping.")
            continue

        # Check if adding one more would exceed max positions
        if len(held_symbols) >= MAX_POSITIONS:
            print(f"🚫 Reached max positions limit ({MAX_POSITIONS}). Stopping.")
            break

        # 1. Download stock data (just this symbol)
        hist_data = get_historical_data([symbol], period=config.YF_PERIOD, interval=config.YF_INTERVAL)

        if symbol not in hist_data or hist_data[symbol].empty:
            print(f"⚠️ No data for {symbol}, skipping.")
            continue

        # 2. Check entry signal
        signals = run_entry_check({symbol: hist_data[symbol]})

        if not signals:
            print(f"❌ No BUY signal for {symbol}")
            continue

        # 3. Place order immediately
        print(f"✅ BUY signal found for {symbol}, sending order...")
        place_entry_orders(signals, allocation_pct=0.1)

    print("\n🎉 Sequential Entry Bot finished.")


if __name__ == "__main__":
    main()