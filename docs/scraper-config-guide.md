# Understanding `scraper_config.py` — A Beginner's Guide

## What is this file?

Think of `scraper_config.py` as a **settings file** for your web scraper.

When you want to grab stock prices from a website, you need to know two things:

1. **Where to look** — the URL (web address) of the page.
2. **What to grab** — which part of the page contains the data you want.

Instead of scattering these details across multiple files, we put them all in one
place. If a website changes its address or its HTML layout, you only fix one file.

---

## Part 1: URLs (Where to look)

### What is a URL?

A URL is just a web address, like `https://www.google.com`. When your Python code
calls `requests.get(url)`, it downloads the HTML of that page — the same HTML your
browser uses to display it.

### Our two data sources

We configured two websites:

| Source | URL | Works with `requests`? |
|--------|-----|----------------------|
| African Markets | `african-markets.com` | Yes |
| Casablanca Bourse (official) | `casablanca-bourse.com` | No (needs Selenium) |

**Why the difference?** When you visit a website:

- Some websites send you a **complete HTML page** (all the data is already in the
  HTML). This is called **server-rendered**. You can download it with `requests.get()`
  and the data is right there.

- Other websites send you a **blank page + JavaScript code**. The JavaScript runs
  in your browser and *then* fills in the data. This is called **client-rendered** or
  **JS-rendered**. If you use `requests.get()`, you get the blank page — no data.
  You need a tool like Selenium (Phase 4) that runs a real browser.

African Markets is server-rendered, so we start with it.

### Base URL vs. full URL

```python
AFRICAN_MARKETS_BASE_URL = "https://www.african-markets.com"

AFRICAN_MARKETS_LISTED_URL = (
    f"{AFRICAN_MARKETS_BASE_URL}/en/stock-markets/bvc/listed-companies"
)
```

We store the **base** (`https://www.african-markets.com`) separately because multiple
URLs share it. Then we build full URLs by appending paths. The `f"..."` is an
f-string — Python replaces `{AFRICAN_MARKETS_BASE_URL}` with its value.

The result is:
```
https://www.african-markets.com/en/stock-markets/bvc/listed-companies
```

### URL templates with placeholders

```python
AFRICAN_MARKETS_COMPANY_URL = (
    f"{AFRICAN_MARKETS_BASE_URL}/en/stock-markets/bvc/listed-companies/company?code={{ticker}}"
)
```

The `{{ticker}}` looks weird. Here's what happens:

- `{{ }}` inside an f-string produces a literal `{ }` (because `{ }` normally
  means "insert a variable", so you double them to escape).
- The result is the string: `.../company?code={ticker}`
- Later, you call `.format(ticker="IAM")` to fill it in:

```python
url = AFRICAN_MARKETS_COMPANY_URL.format(ticker="IAM")
# Result: "https://www.african-markets.com/.../company?code=IAM"
```

This lets you build a URL for any stock by just passing its ticker code.

---

## Part 2: CSS Selectors (What to grab)

### What is HTML?

Every web page is written in HTML. It looks like this:

```html
<table>
  <thead>
    <tr>
      <th>Company</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="/company?code=IAM">Maroc Telecom</a></td>
      <td>95.50</td>
    </tr>
    <tr>
      <td><a href="/company?code=ATW">Attijariwafa Bank</a></td>
      <td>689.00</td>
    </tr>
  </tbody>
</table>
```

Key tags to know:

| Tag | Meaning |
|-----|---------|
| `<table>` | A table |
| `<thead>` | Table header section |
| `<tbody>` | Table body (the actual data rows) |
| `<tr>` | A table **r**ow |
| `<th>` | A header cell (bold text like "Company", "Price") |
| `<td>` | A data cell (the actual value like "Maroc Telecom", "95.50") |
| `<a>` | A link (clickable text) |

### What is a CSS selector?

A CSS selector is a **pattern** that tells BeautifulSoup which HTML elements to find.

| Selector | Finds |
|----------|-------|
| `"table"` | Any `<table>` element |
| `"table tbody tr"` | Any `<tr>` that is inside a `<tbody>` inside a `<table>` |
| `"td"` | Any `<td>` element |
| `"td a"` | Any `<a>` (link) inside a `<td>` |
| `"table.stock-list"` | A `<table>` with `class="stock-list"` |

The space between words means "inside of". So `"table tbody tr"` reads as:
*"find a `<tr>` that's inside a `<tbody>` that's inside a `<table>`."*

### Our selectors dictionary

```python
AFRICAN_MARKETS_SELECTORS = {
    "stock_table": "table",            # find the <table> element
    "table_rows": "table tbody tr",    # find each row in the table body
    "table_cells": "td",               # find each cell in a row
    "company_link": "td a",            # find the link inside a cell
    "columns": ["company", "sector", "price", "change_1d", "ytd", "market_cap", "date"],
}
```

**Why `columns`?** The HTML table doesn't label individual cells. The cells just
appear in order: first cell is the company, second is sector, third is price, etc.
The `columns` list maps each position to a name:

```
Cell 0 → "company"    (e.g. "Maroc Telecom")
Cell 1 → "sector"     (e.g. "Telecom")
Cell 2 → "price"      (e.g. "95.50")
Cell 3 → "change_1d"  (e.g. "-0.21%")
Cell 4 → "ytd"        (e.g. "-12.39%")
Cell 5 → "market_cap" (e.g. "83.95")
Cell 6 → "date"       (e.g. "24/04")
```

This is how your scraper will turn a raw HTML row into a nice Python dictionary:

```python
{"company": "Maroc Telecom", "price": "95.50", "change_1d": "-0.21%", ...}
```

---

## Part 3: Common config

```python
DEFAULT_SOURCE = "african_markets"   # which source to use by default
REQUEST_TIMEOUT = 10                 # max seconds to wait for a response
HEADERS = {
    "User-Agent": "StockTeller/1.0 (educational project)",
}
```

- **`DEFAULT_SOURCE`** — so other files can check which source to use without
  hardcoding it.
- **`REQUEST_TIMEOUT`** — if a website takes longer than 10 seconds to respond,
  give up (prevents your program from hanging forever).
- **`HEADERS`** — when your code visits a website, it sends a "User-Agent" string
  that identifies itself. Some websites block requests that don't have one.
  We set it to something descriptive and honest.

---

## How it all connects

Here's the big picture of how the files work together:

```
scraper_config.py          → stores URLs + selectors (this file)
       ↓
http_client.py             → downloads the HTML from a URL
       ↓
html_parser.py             → reads the HTML, finds the table, extracts data
       ↓
quote_scraper.py (Phase 2) → combines everything: gets URL from config,
                              downloads with http_client, parses with html_parser
```

When you import from `scraper_config`, it looks like this:

```python
from scraper_config import AFRICAN_MARKETS_LISTED_URL, AFRICAN_MARKETS_SELECTORS
from http_client import retry_get

html = retry_get(AFRICAN_MARKETS_LISTED_URL)
# now parse the html using the selectors...
```

---

## Quick glossary

| Term | Plain English |
|------|---------------|
| URL | Web address (like `https://google.com`) |
| HTML | The code that makes up a web page |
| CSS selector | A pattern to find specific parts of an HTML page |
| Server-rendered | The server sends complete HTML (data already included) |
| JS-rendered | The server sends blank HTML + JavaScript that fills in data later |
| f-string | Python string with `f"..."` that lets you insert variables with `{var}` |
| Base URL | The root address of a website (`https://example.com`) |
| Ticker | A short code for a stock (`IAM` = Maroc Telecom, `ATW` = Attijariwafa Bank) |
