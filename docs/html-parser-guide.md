# Understanding `html_parser.py` — A Beginner's Guide

## What does this file do?

When you download a web page, you get a big string of HTML code — thousands of
characters of tags, text, and attributes all mixed together. It's not usable as-is.

`html_parser.py` takes that messy HTML and extracts **just the table data** you
care about, turning it into a clean Python list of dictionaries.

**Input:**  a huge string of raw HTML
**Output:** a clean list like:

```python
[
    {"Company": "Maroc Telecom", "Price": "95.50", "1D": "-0.21%"},
    {"Company": "Attijariwafa Bank", "Price": "689.00", "1D": "-2.96%"},
    ...
]
```

---

## Line-by-line walkthrough

### Line 1: The import

```python
from bs4 import BeautifulSoup
```

**BeautifulSoup** is a Python library that understands HTML. You give it an HTML
string, and it lets you search through it like a tree.

The library is installed as `beautifulsoup4` (with `uv add beautifulsoup4`), but
when you import it in code, it's `from bs4 import BeautifulSoup`. The names don't
match — that's just how the library was designed.

### Lines 4-15: The function signature and docstring

```python
def parse_table(html: str) -> list[dict[str, str]]:
```

Let's break down the type hints:

| Part | Meaning |
|------|---------|
| `html: str` | The function takes one argument, a string |
| `-> list[dict[str, str]]` | It returns a list of dictionaries |
| `dict[str, str]` | Each dictionary has string keys and string values |

So the return type is a **list of dictionaries** — each dictionary is one row of
the table, where the keys are column headers and the values are cell contents.

### Line 16: Creating the soup

```python
soup = BeautifulSoup(html, "html.parser")
```

This is like opening a document in a text editor. You give BeautifulSoup:

1. `html` — the raw HTML string
2. `"html.parser"` — which parser to use (Python's built-in one)

Now `soup` is an object you can search through.

### Lines 17-19: Finding the table

```python
table = soup.find("table")
if table is None:
    return []
```

`soup.find("table")` searches the entire HTML for the **first** `<table>` tag.

- If it finds one, `table` is now that table element.
- If there's no table in the HTML, `table` is `None`, and we return an empty list
  (nothing to parse).

### Lines 21-24: The stub (not finished yet)

```python
headers: list[str] = []
rows: list[dict[str, str]] = []

return rows
```

This is a **stub** — placeholder code that returns an empty list. The function
structure is there, but the logic isn't written yet. That's intentional — the
learning path has you build it step by step.

---

## How the finished version will work

When you complete this function, it will do these steps:

### Step 1: Extract column headers

```
HTML:  <thead><tr><th>Company</th><th>Price</th><th>1D</th></tr></thead>

Python: headers = ["Company", "Price", "1D"]
```

You'll find all `<th>` tags inside the table's `<thead>` and grab their text.

### Step 2: Loop through each data row

```
HTML:  <tbody>
         <tr><td>Maroc Telecom</td><td>95.50</td><td>-0.21%</td></tr>
         <tr><td>Attijariwafa Bank</td><td>689.00</td><td>-2.96%</td></tr>
       </tbody>
```

You'll find all `<tr>` tags inside `<tbody>`.

### Step 3: For each row, pair headers with cell values

For the first row:

```python
cells = ["Maroc Telecom", "95.50", "-0.21%"]
headers = ["Company", "Price", "1D"]

# Pair them up:
row_dict = {
    "Company": "Maroc Telecom",
    "Price": "95.50",
    "1D": "-0.21%",
}
```

Python's `zip()` function is perfect for this — it pairs items from two lists:

```python
zip(["Company", "Price", "1D"], ["Maroc Telecom", "95.50", "-0.21%"])
# → [("Company", "Maroc Telecom"), ("Price", "95.50"), ("1D", "-0.21%")]
```

### Step 4: Collect all row dictionaries into the list

```python
rows.append(row_dict)
```

---

## Key BeautifulSoup methods you'll use

| Method | What it does | Example |
|--------|-------------|---------|
| `soup.find("tag")` | Finds the **first** matching tag | `soup.find("table")` → first table |
| `soup.find_all("tag")` | Finds **all** matching tags (returns a list) | `table.find_all("tr")` → all rows |
| `tag.get_text()` | Gets the visible text inside a tag | `cell.get_text()` → `"95.50"` |
| `tag.get_text(strip=True)` | Same but removes extra whitespace | Useful when HTML has spaces/newlines |

### `find` vs `find_all`

- `find("tr")` → returns **one** element (the first match), or `None`
- `find_all("tr")` → returns a **list** of all matches (could be empty `[]`)

Use `find` when you expect exactly one thing (like the table itself).
Use `find_all` when you expect many things (like all the rows).

---

## Visual example: from HTML to Python

Imagine this is the HTML you downloaded:

```html
<html>
  <body>
    <h1>Stock Prices</h1>
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Maroc Telecom</td>
          <td>95.50</td>
        </tr>
        <tr>
          <td>BCP</td>
          <td>245.00</td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
```

Here's what the finished `parse_table` would do:

```
1. BeautifulSoup(html, "html.parser")       → parses the whole page
2. soup.find("table")                        → finds the <table>
3. table.find_all("th")                      → ["Company", "Price"]
4. table.find("tbody").find_all("tr")        → [<row1>, <row2>]
5. For row1: find_all("td")                  → ["Maroc Telecom", "95.50"]
6. zip(headers, cells)                       → {"Company": "Maroc Telecom", "Price": "95.50"}
7. For row2: find_all("td")                  → ["BCP", "245.00"]
8. zip(headers, cells)                       → {"Company": "BCP", "Price": "245.00"}
```

**Final result:**

```python
[
    {"Company": "Maroc Telecom", "Price": "95.50"},
    {"Company": "BCP", "Price": "245.00"},
]
```

---

## How `html_parser.py` connects to `scraper_config.py`

Right now, `parse_table` uses `soup.find("table")` to find **any** table on the
page. This works if the page has only one table.

But some pages have multiple tables (navigation tables, ad tables, etc.). That's
where the CSS selectors from `scraper_config.py` come in — they help you target
the **exact** table you want:

```python
from bs4 import BeautifulSoup
from scraper_config import AFRICAN_MARKETS_SELECTORS

soup = BeautifulSoup(html, "html.parser")

# Instead of soup.find("table"), use the selector from config:
rows = soup.select(AFRICAN_MARKETS_SELECTORS["table_rows"])
```

`soup.select()` uses CSS selectors (the same ones from `scraper_config.py`) to
find elements. It's more powerful than `find()` because you can target nested
elements in one call.

| Method | Input | Example |
|--------|-------|---------|
| `soup.find("table")` | A tag name | Finds first `<table>` |
| `soup.select("table tbody tr")` | A CSS selector | Finds all `<tr>` inside `<tbody>` inside `<table>` |

---

## Quick glossary

| Term | Plain English |
|------|---------------|
| HTML | The code behind every web page, made of nested tags |
| Tag | An HTML element like `<table>`, `<tr>`, `<td>` |
| BeautifulSoup | A Python library for reading and searching HTML |
| Parser | A tool that reads code and understands its structure |
| Stub | Placeholder code — correct shape, but not finished yet |
| `find()` | Search for the first matching tag |
| `find_all()` | Search for all matching tags |
| `select()` | Search using CSS selectors (more flexible) |
| `get_text()` | Extract the visible text from an HTML tag |
| `zip()` | Python function that pairs items from two lists |
