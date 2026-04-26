import requests

def get_page(url: str) -> str:
    """Get the HTML content of a page."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text