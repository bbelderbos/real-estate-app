""" Base class for real estate website scrapers.
"""
import abc
from dataclasses import dataclass, field
from typing import ClassVar, Generator, List

from bs4 import BeautifulSoup

from http_requests.request import make_request


@dataclass
class Scraper(abc.ABC):
    """ Base class for Real Estate Scraper.
    """

    url: ClassVar[str]
    category_urls: ClassVar[List[str]]
    name: ClassVar[str] = field(init=False)

    def __post_init__(self):
        self.name = self.url.split("//")[-1].split("/")[0].split("?")[0]

    @abc.abstractmethod
    def scrape_all_items(self) -> List[dict]:
        """ scrape and parse all items from starting url.
        """
        pass

    @abc.abstractmethod
    def parse_page_items(self, soup: BeautifulSoup) -> Generator[dict, None, None]:
        """ parse all items showing on a page.
        """
        pass

    @abc.abstractmethod
    def parse_preview_item(self, soup: BeautifulSoup) -> dict:
        """ Parse a preview item that shows up on a result page.
        """
        pass

    @abc.abstractmethod
    def parse_details_page(self, url: str):
        """ Make request to detail page and get the detail data.
        """
        pass

    def ping(self):
        """ Make test request to home page """
        return make_request(self.url)
