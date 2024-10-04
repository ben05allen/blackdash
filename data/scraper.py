from itertools import islice
from lxml import etree
import requests
from typing import Generator


def scrape_tickers(
    url: str, tickers_xpath: str, names_xpath: str, limit: int
) -> Generator[tuple[str, str], None, None]:
    parser = etree.HTMLParser()
    response = requests.get(url)
    root = etree.fromstring(response.content, parser)

    tickers = root.xpath(tickers_xpath)
    names = root.xpath(names_xpath)

    for name, ticker in islice(zip(names, tickers), limit):
        yield (name.strip(), ticker.strip())


if __name__ == "__main__":
    kospi_url = "https://stockanalysis.com/list/korea-stock-exchange/"
    kospi_tickers_xpath = '//td[@class="sym svelte-eurwtr"]/a/text()'
    kospi_names_xpath = '//td[@class="slw svelte-eurwtr"]/text()'
    kospi_limit = 20

    for name, ticker in scrape_tickers(
        kospi_url, kospi_tickers_xpath, kospi_names_xpath, kospi_limit
    ):
        print(f"{name} ({ticker}.KS)")
