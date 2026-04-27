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
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []

    headers: list[str] = []
    rows: list[dict[str, str]] = []

    return rows