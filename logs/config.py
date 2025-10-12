# file: config.py

# --- IBKR connection settings ---
TWS_HOST = "127.0.0.1"  # or "host.docker.internal" if running inside Docker
TWS_PORT = 7497  # 7497 live / 7496 paper / 4002 gateway paper
CLIENT_ID = 5  # change if you want multiple connections
TIMEOUT = 10  # seconds

# --- Risk / Debug options ---
DRY_RUN = True  # if True: do not send real orders, only print
