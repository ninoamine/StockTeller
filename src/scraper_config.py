"""Configuration for Casablanca Stock Exchange scrapers.

Centralizes target URLs and CSS selectors so scraper modules
can import them instead of hardcoding.
"""

# ---------------------------------------------------------------------------
# African Markets -- server-rendered HTML, works with requests + BeautifulSoup
# ---------------------------------------------------------------------------

AFRICAN_MARKETS_BASE_URL = "https://www.african-markets.com"

AFRICAN_MARKETS_LISTED_URL = (
    f"{AFRICAN_MARKETS_BASE_URL}/en/stock-markets/bvc/listed-companies"
)

AFRICAN_MARKETS_COMPANY_URL = (
    f"{AFRICAN_MARKETS_BASE_URL}/en/stock-markets/bvc/listed-companies/company?code={{ticker}}"
)

AFRICAN_MARKETS_SELECTORS = {
    "stock_table": "table",
    "table_rows": "table tbody tr",
    "table_cells": "td",
    "company_link": "td a",
    "columns": ["company", "sector", "price", "change_1d", "ytd", "market_cap", "date"],
}


# ---------------------------------------------------------------------------
# Casablanca Bourse (official) -- JS-rendered, needs Selenium (Phase 4)
# ---------------------------------------------------------------------------

CASABLANCA_BOURSE_BASE_URL = "https://www.casablanca-bourse.com"

CASABLANCA_BOURSE_STOCKS_URL = (
    f"{CASABLANCA_BOURSE_BASE_URL}/fr/live-market/marche-actions-groupement"
)

CASABLANCA_BOURSE_OVERVIEW_URL = (
    f"{CASABLANCA_BOURSE_BASE_URL}/fr/live-market/overview"
)

CASABLANCA_BOURSE_EMETTEUR_URL = (
    f"{CASABLANCA_BOURSE_BASE_URL}/fr/live-market/emetteurs/{{instrument_code}}"
)

CASABLANCA_BOURSE_SELECTORS = {
    "stock_table": "table",
    "table_rows": "table tbody tr",
    "table_cells": "td",
    "columns": [
        "instrument", "status", "reference_price", "opening",
        "last_price", "quantity", "volume", "change_pct",
    ],
}


# ---------------------------------------------------------------------------
# Common config
# ---------------------------------------------------------------------------

DEFAULT_SOURCE = "african_markets"

REQUEST_TIMEOUT = 10

HEADERS = {
    "User-Agent": "StockTeller/1.0 (educational project)",
}