# file: connect_ib.py
import os
from ib_insync import IB

# file: connect_ib.py
from ib_insync import IB
import config


def connect_ib() -> IB:
    ib = IB()

    ib.connect(
        config.TWS_HOST,
        config.TWS_PORT,
        clientId=config.CLIENT_ID,
        timeout=config.TIMEOUT,
    )
    _ = ib.reqCurrentTime()  # simple test
    return ib


def disconnect_ib(ib: IB) -> None:
    if ib and ib.isConnected():
        ib.disconnect()


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
