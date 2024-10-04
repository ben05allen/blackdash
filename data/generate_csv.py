import asyncio
import csv
from dataclasses import dataclass
import httpx
from itertools import islice
from lxml import etree
import tomllib
from typing import AsyncGenerator

CSV_FILE = "data/test.csv"


@dataclass
class ExchangeMeta:
    stockindex: str
    exchange: str
    currency: str
    url: str
    tickers_xpath: str
    names_xpath: str
    ticker_suffix: str
    limit: int


@dataclass
class Ticker:
    name: str
    symbol: str
    stockindex: str
    exchange: str
    currency: str


async def scrape_tickers(
    client, url: str, tickers_xpath: str, names_xpath: str, limit: int
) -> AsyncGenerator[tuple[str, str], None]:
    parser = etree.HTMLParser()
    response = await client.get(url)
    root = etree.fromstring(response.content, parser)
    tickers = root.xpath(tickers_xpath)
    names = root.xpath(names_xpath)

    return [(n, t) for n, t in islice(zip(names, tickers), limit)]


async def create_exch_list(client, meta: ExchangeMeta) -> list[Ticker]:
    exchange_list = []
    tickers_list = await scrape_tickers(
        client, meta.url, meta.tickers_xpath, meta.names_xpath, meta.limit
    )
    for name, ticker in tickers_list:
        exchange_list.append(
            Ticker(
                name,
                f"{ticker}{meta.ticker_suffix}",
                meta.stockindex,
                meta.exchange,
                meta.currency,
            )
        )
    return exchange_list


async def gather_data() -> list[list[Ticker]]:
    with open("data/exchanges.toml", "rb") as f:
        exch_data = tomllib.load(f)

    async with httpx.AsyncClient() as client:
        tasks = [
            create_exch_list(client, ExchangeMeta(**exch))
            for exch in exch_data.values()
        ]
        return await asyncio.gather(*tasks)


def write_csv(exchanges_data: list[list]) -> None:
    with open(CSV_FILE, "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=Ticker.__dataclass_fields__)
        csv_writer.writeheader()

        for exchange_list in exchanges_data:
            for ticker in exchange_list:
                csv_writer.writerow(ticker.__dict__)


async def main() -> None:
    exchanges_data = await gather_data()
    write_csv(exchanges_data)


if __name__ == "__main__":
    asyncio.run(main())
