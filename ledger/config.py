# file: config.py

# --- IBKR connection settings ---
TWS_HOST = "127.0.0.1"  # or "host.docker.internal" if running inside Docker
TWS_PORT = 4002  # 7497 live / 7496 paper / 4002 gateway paper
CLIENT_ID = 4  # change if you want multiple connections
TIMEOUT = 10  # seconds
