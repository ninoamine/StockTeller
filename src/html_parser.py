from bs4 import BeautifulSoup


def parse_table(html: str) -> list[dict[str, str]]:
    """Parse an HTML table into a list of dictionaries.
    
    Each dictionnary represents a row, with column headers as keys
    and cell text as values.

    Args:
        html: the HTML content to parse

    Returns:
        a list of dictionaries, each representing a row in the table
    """
    rows: list[dict[str, str]] = []
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []

    header_tags = table.find_all("th")
    headers = [header.get_text(strip=True) for header in header_tags]


    tbody = table.find("tbody")
    if tbody is None:
        return []
    
    for tr in tbody.find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) != len(headers):
            continue
        row = {}
        for key, td in zip(headers, cells):
            row[key] = td.get_text(strip=True)
        rows.append(row)

    return rows