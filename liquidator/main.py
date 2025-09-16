from ib_insync import MarketOrder
from connect_ib import connect_ib, disconnect_ib
import config


def close_all_positions():
    ib = connect_ib()
    portfolio = ib.portfolio()
    if not portfolio:
        print("📭 No open positions.")
        disconnect_ib(ib)
        return

    print("\n🔒 Closing all open positions...")
    for p in portfolio:
        symbol = p.contract.symbol
        qty = p.position
        if qty != 0:
            action = "SELL" if qty > 0 else "BUY"
            order = MarketOrder(action, abs(qty))
            if config.DRY_RUN:
                print(
                    f"⚠️ DRY RUN: Would send {order.action} order to close {qty} {symbol}"
                )
            else:
                try:
                    ib.qualifyContracts(p.contract)
                    ib.placeOrder(p.contract, order)
                    print(f"➡️ Sent {order.action} order to close {qty} {symbol}")
                except Exception as e:
                    print(f"❌ Error closing {symbol}: {e}")
    disconnect_ib(ib)


if __name__ == "__main__":
    close_all_positions()
