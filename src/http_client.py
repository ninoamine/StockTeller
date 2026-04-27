import requests, time

def get_page(url: str) -> str:
    """Get the HTML content of a page."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def retry_get(url: str, retries: int = 3) -> str:
    """Retry a GET request up to a maximum number of times."""
    for i in range(retries):
        try:
            return get_page(url)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code < 500:
                raise
            if i == retries - 1:
                raise
            time.sleep(2 ** i)
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)
