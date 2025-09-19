from ib_insync import MarketOrder
from connect_ib import connect_ib, disconnect_ib


def close_all_positions():
    ib = connect_ib()
    portfolio = ib.portfolio()
    if not portfolio:
        disconnect_ib(ib)
        return

    for p in portfolio:
        symbol = p.contract.symbol
        qty = p.position
        if qty != 0:
            action = "SELL" if qty > 0 else "BUY"
            order = MarketOrder(action, abs(qty))
            try:
                ib.qualifyContracts(p.contract)
                ib.placeOrder(p.contract, order)
            except Exception as e:
                print(f"❌ Error closing {symbol}: {e}")
    disconnect_ib(ib)


if __name__ == "__main__":
    close_all_positions()
