# file: data_fetch.py
import yfinance as yf
import pandas as pd
import config

def get_historical_data(tickers, period=None, interval=None):
    """
    Download historical OHLCV data for each ticker.
    Returns {ticker: DataFrame}
    """
    period   = period or config.YF_PERIOD
    interval = interval or config.YF_INTERVAL

    if not tickers:
        print("⚠️ No tickers provided for historical data fetch.")
        return {}

    print(f"\n📥 Downloading historical data (period={period}, interval={interval})...")
    data = {}
    for symbol in tickers:
        try:
            df = yf.download(symbol, period=period, interval=interval,
                             auto_adjust=True, progress=False)

            # flatten MultiIndex if needed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            if not df.empty:
                data[symbol] = df
                print(f"✅ {symbol}: {len(df)} rows retrieved")
            else:
                print(f"⚠️ {symbol}: no data retrieved")
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
    return data

# Run standalone for quick test
if __name__ == "__main__":
    # Example test (replace with tickers you know exist in your account)
    test_tickers = ["AAPL", "MSFT"]
    hist_data = get_historical_data(test_tickers, period="1mo", interval="1d")

    for t, df in hist_data.items():
        print(f"\n📈 {t} (last 5 rows):")
        print(df.tail())
