# file: atr_check.py
import backtrader as bt
import pandas as pd
import config

class ATRStrategy(bt.Strategy):
    params = dict(period=config.ATR_PERIOD, atr_mult=config.ATR_MULT)

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.p.period)

    def next(self):
        last_close = self.data.close[0]
        last_atr   = self.atr[0]
        exit_level = last_close - self.p.atr_mult * last_atr

        self.signal     = "exit" if last_close < exit_level else "hold"
        self.last_close = last_close
        self.last_atr   = last_atr
        self.exit_level = exit_level

def run_atr_check(hist_data, atr_period=config.ATR_PERIOD, atr_mult=config.ATR_MULT):
    """
    Run ATR check for each ticker using Backtrader.
    Returns {ticker: {...}}
    """
    results = {}

    for symbol, df in hist_data.items():
        df = df.copy()
        df.index = pd.to_datetime(df.index)

        data = bt.feeds.PandasData(dataname=df)

        cerebro = bt.Cerebro()
        cerebro.addstrategy(ATRStrategy)
        cerebro.adddata(data)

        strategies = cerebro.run()
        strat = strategies[0]

        results[symbol] = {
            "close": strat.last_close,
            "atr": strat.last_atr,
            "exit_level": strat.exit_level,
            "signal": strat.signal
        }

        print(f"\n📈 {symbol}: Close={strat.last_close:.2f}, ATR={strat.last_atr:.2f}, "
              f"Exit={strat.exit_level:.2f}, Signal={strat.signal.upper()}")

    return results

# Run standalone for quick test
if __name__ == "__main__":
    import yfinance as yf
    from data_fetch import get_historical_data

    test_tickers = ["AAPL"]
    hist_data = get_historical_data(test_tickers, period="1mo", interval="1d")
    signals = run_atr_check(hist_data, atr_period=14, atr_mult=1.0)

    print("\n📊 Summary:", signals)