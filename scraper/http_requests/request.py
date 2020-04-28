from typing import Optional
import requests


DEFAULT_HEADERS = {
    "User-Agent": ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/74.0.3729.169 Safari/537.36')
}


def make_request(url: str, headers: Optional[dict] = None,
                 proxies: Optional[dict] = None) -> Optional[requests.Response]:
    """ Make HTTP Get Request, return response if status code is 200,
    none if 404 else raise error.
    """
    if headers is None:
        headers = DEFAULT_HEADERS
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
    except requests.exceptions.MissingSchema:
        raise ValueError("Incorrect URL provided.")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response
