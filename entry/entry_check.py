# file: entry_check.py
import config


def compute_bollinger_bands(df, period=20, num_std=2):
    """
    Compute Bollinger Bands for a given DataFrame (must have 'Close').
    Returns df with 'BB_Mid', 'BB_Upper', 'BB_Lower' columns.
    """
    df = df.copy()
    df["BB_Mid"] = df["Close"].rolling(window=period).mean()
    df["BB_Std"] = df["Close"].rolling(window=period).std()
    df["BB_Upper"] = df["BB_Mid"] + num_std * df["BB_Std"]
    df["BB_Lower"] = df["BB_Mid"] - num_std * df["BB_Std"]
    return df


def run_entry_check(hist_data, bb_period=20, bb_std=2):
    """
    Run Bollinger Band breakout check.
    Keeps only BUY signals (close > upper band).
    Returns dict {ticker: {"close": last_close, "signal": "buy"}}
    """
    buy_signals = {}

    for symbol, df in hist_data.items():
        if df.empty or "Close" not in df.columns:
            continue

        df = compute_bollinger_bands(df, period=bb_period, num_std=bb_std)

        last_close = df["Close"].iloc[-1]
        upper_band = df["BB_Upper"].iloc[-1]

        if last_close > upper_band:  # breakout above upper band
            buy_signals[symbol] = {"close": last_close, "signal": "buy"}

    return buy_signals


# Standalone test
if __name__ == "__main__":
    from tickers import load_tickers
    from data_fetch import get_historical_data

    tickers = load_tickers("stocks.txt")
    hist_data = get_historical_data(
        tickers, period=config.YF_PERIOD, interval=config.YF_INTERVAL
    )
    signals = run_entry_check(hist_data)

    # print("\n📊 Final BUY Signals:", signals)
