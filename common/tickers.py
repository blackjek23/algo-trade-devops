# file: tickers.py


def load_tickers(filename="stocks.txt"):
    """
    Load ticker symbols from a text file.
    One ticker per line.
    Returns a list of symbols.
    """
    try:
        with open(filename, "r") as f:
            tickers = [line.strip().upper() for line in f if line.strip()]
        print(f"✅ Loaded {len(tickers)} tickers from {filename}")
        return tickers
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return []
