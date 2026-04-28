from http_client import retry_get
from scraper_config import AFRICAN_MARKETS_LISTED_URL, AFRICAN_MARKETS_SELECTORS
from bs4 import BeautifulSoup


def scrape_one_quote(ticker: str) -> dict[str, str]:
    listed_companies = retry_get(AFRICAN_MARKETS_LISTED_URL)
    soup = BeautifulSoup(listed_companies, "html.parser")
    table_rows= soup.select(AFRICAN_MARKETS_SELECTORS["table_rows"])
    for row in table_rows:
        company_link = row.select_one(AFRICAN_MARKETS_SELECTORS["company_link"])
        if company_link is None:
            continue
        href = company_link.get("href", "")
        if f"?code={ticker}" in href:
            cells = row.find_all("td")
            return {
                "name": cells[0].get_text(strip=True),
                "price": cells[2].get_text(strip=True),
                "change_pct": cells[3].get_text(strip=True),
            }
    raise ValueError(f"Ticker '{ticker}' not found")
