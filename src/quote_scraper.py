"""Scrape individual stock quotes from the African Markets listed-companies page.

The page at african-markets.com/en/stock-markets/bvc/listed-companies renders a
server-side HTML ``<table>`` with one row per company.  Each ``<tr>`` contains
seven ``<td>`` cells whose column order is defined in
``scraper_config.AFRICAN_MARKETS_SELECTORS["columns"]``::

    [company, sector, price, change_1d, ytd, market_cap, date]

This module relies purely on CSS selectors (no XPath) to navigate that table.
"""

from http_client import retry_get
from scraper_config import AFRICAN_MARKETS_LISTED_URL, AFRICAN_MARKETS_SELECTORS
from bs4 import BeautifulSoup


def scrape_one_quote(ticker: str) -> dict[str, str]:
    """Return name, price, and daily change for *ticker*.

    **CSS selectors used (all defined in ``scraper_config``):**

    ``"table tbody tr"`` (key ``table_rows``)
        Selects every ``<tr>`` inside the ``<tbody>`` of the first ``<table>``
        on the page.  Each row represents one listed company.  We skip the
        ``<thead>`` header row automatically because ``<thead>`` is a sibling
        of ``<tbody>``, not a child.

    ``"td a"`` (key ``company_link``)
        Inside each row, selects the first ``<a>`` anchor nested in a ``<td>``
        cell.  The anchor's ``href`` contains a query parameter
        ``?code=<TICKER>`` that uniquely identifies the company, e.g.
        ``/en/stock-markets/bvc/listed-companies/company?code=IAM``.

    ``row.find_all("td")``
        After matching the ticker, we grab *all* ``<td>`` cells in the row.
        Cells are ordered as:

        * ``cells[0]`` -- company name (plain text inside the ``<a>`` tag)
        * ``cells[1]`` -- sector (not used here)
        * ``cells[2]`` -- last traded price
        * ``cells[3]`` -- one-day percentage change
        * ``cells[4..6]`` -- YTD change, market cap, date (not used here)

    Raises:
        ValueError: If *ticker* is not found in any table row.
    """
    listed_companies = retry_get(AFRICAN_MARKETS_LISTED_URL)
    soup = BeautifulSoup(listed_companies, "html.parser")
    table_rows = soup.select(AFRICAN_MARKETS_SELECTORS["table_rows"])
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
