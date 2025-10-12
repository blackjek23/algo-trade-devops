from connect_ib import connect_ib, disconnect_ib
from logger import log_portfolio_state


def get_open_tickers():
    """
    Fetch open positions from IBKR.
    Returns a list of holdings dicts, each with:
        symbol (str): Ticker symbol
        qty (float): Position size
        pnl (float): Unrealized P&L
    Example:
        [
            {"symbol": "AAPL", "qty": 100, "pnl": 500.0},
            {"symbol": "MSFT", "qty": 50, "pnl": 200.0}
        ]
    """
    ib = connect_ib()
    open_positions = []
    free_cash = ib.accountSummary()[31].value
    UnrealizedPnL = ib.accountSummary()[39].value
    portfolio_value = ib.accountSummary()[34].value

    try:
        portfolio = ib.portfolio()
        if not portfolio:
            print("📭 No open positions found.")
        else:
            for pos in portfolio:
                symbol = pos.contract.symbol
                qty = pos.position
                pnl = pos.unrealizedPNL
                holdings = {
                    "symbol": symbol,
                    "qty": qty,
                    "pnl": pnl,
                }
                open_positions.append(holdings)

    except Exception as e:
        print(f"❌ Error fetching positions: {e}")

    disconnect_ib(ib)
    return open_positions, free_cash, UnrealizedPnL, portfolio_value


# Standalone test
if __name__ == "__main__":
    positions = get_open_tickers()
    # Example summary, replace with real values as needed
    summary = {
        "sum_pnl": positions[2],
        "free_cash": positions[1],
        "portfolio_value": positions[3],
    }

    log_portfolio_state(positions[0], summary)
