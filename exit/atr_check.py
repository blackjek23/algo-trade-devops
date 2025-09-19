# file: atr_check.py
import backtrader as bt
import pandas as pd
import config


class ATRExitStrategy(bt.Strategy):
    params = dict(period=config.ATR_PERIOD, atr_mult=config.ATR_MULT)

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.p.period)
        self.stop_level = None  # persistent trailing stop

    def next(self):
        last_close = self.data.close[0]
        last_atr = self.atr[0]

        # Initial stop (first calculation)
        if self.stop_level is None:
            self.stop_level = last_close - self.p.atr_mult * last_atr

        # Update trailing stop: only move it UP, never down
        new_stop = last_close - self.p.atr_mult * last_atr
        self.stop_level = max(self.stop_level, new_stop)

        # Check for exit
        if last_close < self.stop_level:
            self.signal = "exit"
        else:
            self.signal = "hold"

        # Save values for reporting
        self.last_close = last_close
        self.last_atr = last_atr


def run_atr_exit_check(
    hist_data, atr_period=config.ATR_PERIOD, atr_mult=config.ATR_MULT
):
    """
    Run ATR trailing stop check for each ticker using Backtrader.
    Returns {ticker: {...}}
    """
    results = {}

    for symbol, df in hist_data.items():
        df = df.copy()
        df.index = pd.to_datetime(df.index)

        data = bt.feeds.PandasData(dataname=df)

        cerebro = bt.Cerebro()
        cerebro.addstrategy(ATRExitStrategy, period=atr_period, atr_mult=atr_mult)
        cerebro.adddata(data)

        strategies = cerebro.run()
        strat = strategies[0]

        results[symbol] = {
            "close": strat.last_close,
            "atr": strat.last_atr,
            "stop_level": strat.stop_level,
            "signal": strat.signal,
        }

        return results


# Run standalone for quick test
if __name__ == "__main__":
    import yfinance as yf
    from data_fetch import get_historical_data

    test_tickers = ["AAPL"]
    hist_data = get_historical_data(test_tickers, period="6mo", interval="1d")

    signals = run_atr_exit_check(hist_data, atr_period=14, atr_mult=1.5)

    # print("\n📊 Summary:", signals)
