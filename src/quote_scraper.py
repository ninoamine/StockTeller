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
from bs4 import BeautifulSoup, Tag

COLUMNS = AFRICAN_MARKETS_SELECTORS["columns"]
EXPECTED_CELLS = len(COLUMNS)


def _fetch_table_rows() -> list[Tag]:
    """Fetch the listed-companies page and return all ``<tr>`` elements.

    Shared by :func:`scrape_one_quote` and :func:`scrape_all_quotes` so the
    fetch-parse-select logic lives in one place.
    """
    html = retry_get(AFRICAN_MARKETS_LISTED_URL)
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(AFRICAN_MARKETS_SELECTORS["table_rows"])


def _extract_ticker(link: Tag) -> str:
    """Pull the ticker code from a company link's ``?code=`` query param."""
    href = link.get("href", "")
    if "?code=" in href:
        return href.split("?code=")[-1]
    return ""


def _row_to_dict(row: Tag, link: Tag) -> dict[str, str]:
    """Convert one ``<tr>`` into a dict keyed by the column names in config.

    Returns an empty dict if the row has fewer cells than expected.
    """
    cells = row.find_all("td")
    if len(cells) < EXPECTED_CELLS:
        return {}
    quote = {"ticker": _extract_ticker(link)}
    for key, cell in zip(COLUMNS, cells):
        quote[key] = cell.get_text(strip=True)
    return quote


def scrape_one_quote(ticker: str) -> dict[str, str]:
    """Return the full row of data for *ticker*.

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
        Cells are ordered as defined in
        ``scraper_config.AFRICAN_MARKETS_SELECTORS["columns"]``:

        * ``cells[0]`` -- company name (plain text inside the ``<a>`` tag)
        * ``cells[1]`` -- sector
        * ``cells[2]`` -- last traded price
        * ``cells[3]`` -- one-day percentage change
        * ``cells[4]`` -- year-to-date change
        * ``cells[5]`` -- market capitalisation
        * ``cells[6]`` -- date

    Raises:
        ValueError: If *ticker* is not found in any table row.
    """
    for row in _fetch_table_rows():
        link = row.select_one(AFRICAN_MARKETS_SELECTORS["company_link"])
        if link is None:
            continue
        if _extract_ticker(link) == ticker:
            quote = _row_to_dict(row, link)
            if quote:
                return quote
    raise ValueError(f"Ticker '{ticker}' not found")


def scrape_all_quotes() -> list[dict[str, str]]:
    """Parse the full listed-companies table into a list of dicts.

    Each dict contains a ``"ticker"`` key (extracted from the company link's
    ``?code=`` parameter) plus one key per column defined in
    ``scraper_config.AFRICAN_MARKETS_SELECTORS["columns"]``::

        {"ticker": "IAM", "company": "Maroc Telecom", "sector": "Telecom",
         "price": "125.00", "change_1d": "-0.40%", "ytd": "3.20%",
         "market_cap": "110 000 000 000", "date": "30/04/2026"}

    Rows with fewer cells than expected are silently skipped.
    """
    quotes = []
    for row in _fetch_table_rows():
        link = row.select_one(AFRICAN_MARKETS_SELECTORS["company_link"])
        if link is None:
            continue
        quote = _row_to_dict(row, link)
        if quote:
            quotes.append(quote)
    return quotes