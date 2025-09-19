# file: common/positions.py
from connect_ib import connect_ib, disconnect_ib


def get_open_tickers(verbose=False):
    """
    Fetch open positions from IBKR.
    Returns a dict {symbol: {"qty": float, "avgCost": float, "marketPrice": float}}
    """
    ib = connect_ib()
    open_positions = {}

    try:
        positions = ib.positions()
        for pos in positions:
            symbol = pos.contract.symbol
            open_positions[symbol] = {"qty": pos.position, "avgCost": pos.avgCost}
    except Exception as e:
        print(f"❌ Error fetching positions: {e}")

    disconnect_ib(ib)
    return open_positions


# Standalone test
if __name__ == "__main__":
    positions = get_open_tickers(verbose=True)
    # print("\n✅ Open Positions Dict:", positions)
