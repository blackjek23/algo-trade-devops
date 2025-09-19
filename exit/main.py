# file: main.py
import config
from positions import get_open_tickers
from data_fetch import get_historical_data
from atr_check import run_atr_exit_check
from close_orders import close_positions


def main():

    # 1) Get open positions
    open_positions = get_open_tickers()  # returns {symbol: {...}}
    held_symbols = list(open_positions.keys())

    if not held_symbols:
        return

    # 2) Process each open position one by one
    for symbol in held_symbols:

        # 3) Download stock data (just this symbol)
        hist_data = get_historical_data(
            [symbol], period=config.YF_PERIOD, interval=config.YF_INTERVAL
        )
        df = hist_data.get(symbol)
        if df is None or df.empty:
            continue

        # 4) Run ATR exit check for THIS symbol only
        result = run_atr_exit_check({symbol: df})
        info = result.get(symbol)
        if not info:
            continue

        # Decide here: exit vs hold
        if info["signal"] != "exit":
            continue

        # 5) Place close order immediately (only for this symbol)

        close_positions({symbol: info})


if __name__ == "__main__":
    main()
