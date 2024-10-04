from itertools import islice
from lxml import etree
import requests
from typing import Generator


URL = "https://stockanalysis.com/list/korea-stock-exchange/"
LIMIT = 5


def scrape_tickers(url: str, limit: int) -> Generator[tuple[str, str], None, None]:
    response = requests.get(URL)
    parser = etree.HTMLParser()
    root = etree.fromstring(response.content, parser)

    tickers = root.xpath('//td[@class="sym svelte-eurwtr"]/a/text()')
    names = root.xpath('//td[@class="slw svelte-eurwtr"]/text()')

    for name, ticker in islice(zip(names, tickers), limit):
        yield (name.strip(), ticker.strip())


if __name__ == "__main__":
    for name, ticker in scrape_tickers(URL, LIMIT):
        print(f"{name} ({ticker}.KS)")
