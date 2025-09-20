import pandas as pd

# o= Opening Trade
# p= Partial Execution
# c= Closing Trade

column_names = [
    "Trades",
    "Header",
    "DataDiscriminator",
    "Asset Category",
    "Currency",
    "Account",
    "Symbol",
    "Date/Time",
    "Quantity",
    "T. Price",
    "C. Price",
    "Proceeds",
    "Comm/Fee",
    "Basis",
    "Realized P/L",
    "MTM P/L",
    "Code",
]


# sort by date
def sort_by_date():
    df = pd.read_csv("ledger/trade_rows.csv", names=column_names)
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    df_sorted = df.sort_values("Date/Time")
    return df_sorted


if __name__ == "__main__":
    df_sorted = sort_by_date()
    df_sorted.to_csv("ledger/trade_rows.csv", index=False)
