from itertools import islice
from lxml import etree
import requests
from typing import Generator


# Unfortunately we're not getting purely KOSPI tickers....
# For example Hyundai's ticker comes back as HYMTF rather than 005380.KS

URL = "https://companiesmarketcap.com/south-korea/largest-companies-in-south-korea-by-market-cap/"
COMPANIES = 5


def scrape_tickers(url: str, limit: int) -> Generator[tuple[str, str], None, None]:
    response = requests.get(url)
    parser = etree.HTMLParser()
    root = etree.fromstring(response.content, parser)

    company_name = root.xpath('//div[@class="company-name"]/text()')
    company_code = root.xpath('//div[@class="company-code"]/text()')

    for name, code in islice(zip(company_name, company_code), limit):
        yield (name.strip(), code.strip())


if __name__ == "__main__":
    for name, code in scrape_tickers(URL, COMPANIES):
        print(f"{name} ({code})")
