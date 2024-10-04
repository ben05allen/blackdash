import httpx
from itertools import islice
from lxml import etree


async def scrape_tickers(
    url: str, tickers_xpath: str, names_xpath: str, limit: int
) -> list[tuple[str, str]]:
    parser = etree.HTMLParser()
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        root = etree.fromstring(response.content, parser)
        tickers = root.xpath(tickers_xpath)
        names = root.xpath(names_xpath)

        return [(n, t) for n, t in islice(zip(names, tickers), limit)]
