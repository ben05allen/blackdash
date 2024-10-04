import csv
import tomllib

from scraper import scrape_tickers

CSV_FILE = "data/test.csv"
CSV_FIELDS = [
    "symbol",
    "name",
    "stockindex",
    "exchange",
    "currency",
]


with open("data/exchanges.toml", "rb") as exchanges_file, open(
    CSV_FILE, "w"
) as csv_file:
    exchanges = tomllib.load(exchanges_file)
    csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    csv_writer.writeheader()

    for exch_details in exchanges.values():
        company = dict.fromkeys(CSV_FIELDS)
        company["stockindex"] = exch_details["StockIndex"]
        company["exchange"] = exch_details["Exchange"]
        company["currency"] = exch_details["Currency"]

        for name, ticker in scrape_tickers(
            exch_details["URL"],
            exch_details["TickersXPath"],
            exch_details["NamesXPath"],
            exch_details["Limit"],
        ):
            company["symbol"] = f"{ticker}{exch_details.get('TickerSuffix','')}"
            company["name"] = name
            csv_writer.writerow(company)
