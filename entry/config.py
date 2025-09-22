# file: config.py

# --- IBKR connection settings ---
TWS_HOST = "127.0.0.1"  # or "host.docker.internal" if running inside Docker
TWS_PORT = 4002  # 7497 live / 7496 paper / 4002 gateway paper
CLIENT_ID = 2  # change if you want multiple connections
TIMEOUT = 10  # seconds

# --- Yahoo Finance (yfinance) data settings ---
YF_PERIOD = "3mo"  # e.g., "1mo", "3mo", "6mo", "1y", "2y"
YF_INTERVAL = "1d"  # e.g., "1d", "1h", "5m"

# --- ATR exit strategy settings ---
ATR_PERIOD = 14  # number of candles for ATR
ATR_MULT = 1.0  # multiplier (e.g., 1.0 = 1xATR, 2.0 = 2xATR)

# --- Risk / Debug options ---
DRY_RUN = False  # if True: do not send real orders, only print
