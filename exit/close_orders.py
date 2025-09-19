# file: close_orders.py
from ib_insync import MarketOrder
from connect_ib import connect_ib, disconnect_ib
import config


def close_positions(signals):
    ib = connect_ib()
    portfolio = ib.portfolio()
    if not portfolio:
        disconnect_ib(ib)
        return

    for p in portfolio:
        symbol = p.contract.symbol
        qty = p.position
        sig = signals.get(symbol, {}).get("signal")

        if sig == "exit" and qty != 0:
            if qty > 0:
                order = MarketOrder("SELL", qty)
            else:
                order = MarketOrder("BUY", abs(qty))
            try:
                ib.qualifyContracts(p.contract)
                ib.placeOrder(p.contract, order)
                print(f"➡️ Sent {order.action} order to close {qty} {symbol}")
            except Exception as e:
                print(f"❌ Error closing {symbol}: {e}")

    disconnect_ib(ib)


# Run standalone for quick test
if __name__ == "__main__":
    # Example: pretend ATR signals
    test_signals = {"AAPL": {"signal": "exit"}, "MSFT": {"signal": "hold"}}
    close_positions(test_signals)
