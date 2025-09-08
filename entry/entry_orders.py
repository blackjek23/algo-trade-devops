# file: entry_orders.py
from ib_insync import Stock, MarketOrder
from connect_ib import connect_ib, disconnect_ib
import config

def place_entry_orders(buy_signals, allocation_pct=0.1):
    """
    Place market BUY orders for tickers in buy_signals.
    buy_signals = {ticker: {"close": last_close, "signal": "buy"}}
    - allocation_pct: fraction of NetLiquidation to invest per trade (e.g., 0.1 = 10%)
    """
    if not buy_signals:
        print("📭 No BUY signals, nothing to do.")
        return

    ib = connect_ib()

    # --- Get account value for sizing ---
    account_summary = {v.tag: v.value for v in ib.accountValues()}
    net_liq = float(account_summary.get("NetLiquidation", 0))
    if net_liq <= 0:
        print("⚠️ Could not fetch account NetLiquidation value. Defaulting to $100,000")
        net_liq = 100000.0

    allocation = net_liq * allocation_pct
    print(f"\n💰 NetLiquidation={net_liq:.2f}, Allocation per trade={allocation:.2f}")

    for symbol, info in buy_signals.items():
        if info.get("signal") != "buy":
            continue

        try:
            last_price = info.get("close")
            if not last_price or last_price <= 0:
                print(f"⚠️ Invalid price for {symbol}, skipping.")
                continue

            # Calculate quantity
            qty = int(allocation / last_price)
            if qty <= 0:
                print(f"⚠️ Allocation too small for {symbol}, skipping.")
                continue

            contract = Stock(symbol, "SMART", "USD")
            order = MarketOrder("BUY", qty)

            if config.DRY_RUN:
                print(f"⚠️ DRY RUN: Would BUY {qty} shares of {symbol} at ~{last_price:.2f}")
            else:
                ib.qualifyContracts(contract)
                ib.placeOrder(contract, order)
                print(f"✅ Sent BUY order: {qty} {symbol} at ~{last_price:.2f}")

        except Exception as e:
            print(f"❌ Error placing order for {symbol}: {e}")

    disconnect_ib(ib)

# Standalone test
if __name__ == "__main__":
    # Pretend signals from entry_check.py
    test_signals = {
        "AAPL": {"close": 192.50, "signal": "buy"},
        "MSFT": {"close": 330.40, "signal": "hold"}
    }
    place_entry_orders(test_signals, allocation_pct=0.05)
