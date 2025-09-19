import csv


def get_trade_row():
    with open("ledger/sample.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == "Trades" and row[1] == "Data":
                save_trade_row(row)


def save_trade_row(row):
    with open("ledger/trade_rows.csv", "a", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row)


if __name__ == "__main__":
    get_trade_row()
