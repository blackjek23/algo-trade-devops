# file: main.py
import config
# use the function that returns a dict of positions {symbol: {...}}
from positions import get_open_tickers
from data_fetch import get_historical_data
from atr_check import run_atr_check
from close_orders import close_positions

def main():
    print("🚀 Starting Sequential Exit Bot")

    # 1) Get open positions
    open_positions = get_open_tickers()  # returns {symbol: {...}}
    held_symbols = list(open_positions.keys())

    if not held_symbols:
        print("📭 No open positions. Nothing to check.")
        return

    print(f"📋 {len(held_symbols)} open positions found: {', '.join(held_symbols)}")

    # 2) Process each open position one by one
    for symbol in held_symbols:
        print(f"\n--- 🔍 Checking {symbol} ---")

        # 3) Download stock data (just this symbol)
        hist_data = get_historical_data([symbol], period=config.YF_PERIOD, interval=config.YF_INTERVAL)
        df = hist_data.get(symbol)
        if df is None or df.empty:
            print(f"⚠️ No data for {symbol}, skipping.")
            continue

        # 4) Run ATR exit check for THIS symbol only
        result = run_atr_check({symbol: df})
        info = result.get(symbol)
        if not info:
            print(f"⚠️ No ATR result for {symbol}, skipping.")
            continue

        # Decide here: exit vs hold
        if info["signal"] != "exit":
            print(f"✅ No EXIT for {symbol} "
                  f"(Close={info['close']:.2f}, ATR={info['atr']:.2f}, Exit={info['exit_level']:.2f})")
            continue

        # 5) Place close order immediately (only for this symbol)
        print(f"❌ EXIT signal for {symbol} → sending close order...")
        close_positions({symbol: info})

    print("\n🎉 Sequential Exit Bot finished.")

if __name__ == "__main__":
    main()
