import pandas as pd


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

# o= Opening Trade
# p= Partial Execution
# c= Closing Trade

# sort by date
df = pd.read_csv("ledger/trade_rows.csv", names=column_names)
df["Date/Time"] = pd.to_datetime(df["Date/Time"])
df_sorted = df.sort_values("Date/Time")
