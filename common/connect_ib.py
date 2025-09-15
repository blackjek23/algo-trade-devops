# file: connect_ib.py
from ib_insync import IB
import config


def connect_ib() -> IB:
    ib = IB()
    print(
        f"🔌 Connecting to IBKR at {config.TWS_HOST}:{config.TWS_PORT} (clientId={config.CLIENT_ID}) ..."
    )
    ib.connect(
        config.TWS_HOST,
        config.TWS_PORT,
        clientId=config.CLIENT_ID,
        timeout=config.TIMEOUT,
    )
    _ = ib.reqCurrentTime()  # simple test
    print("✅ Connected.")
    return ib


def disconnect_ib(ib: IB) -> None:
    if ib and ib.isConnected():
        print("🔌 Disconnecting...")
        ib.disconnect()
        print("✅ Disconnected.")


# Run standalone for quick connection test
if __name__ == "__main__":
    import sys

    try:
        ib = connect_ib()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    finally:
        disconnect_ib(locals().get("ib"))
