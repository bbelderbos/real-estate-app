""" Base class for real estate website scrapers.
"""
import abc
from dataclasses import dataclass, field
from typing import ClassVar, Generator, List, Optional

from bs4 import BeautifulSoup

from http_requests.request import make_request

from data.db_session import DbSession
from data.rent_property import RentProperty


def _filter_out_items_already_in_db(lst: List[dict]) -> Generator[dict, None, None]:
    """ Filters out items with id that is already in database.
    """
    session = DbSession.factory()
    for item in lst:
        if not session.query(RentProperty).filter(item['id'] == RentProperty.id).first():
            yield item


def _add_items_to_db(lst: List[dict]) -> List[RentProperty]:
    """ Bulk insert list of property dicts to db.
    """
    items = [RentProperty(**item) for item in lst]
    session = DbSession.factory()
    session.bulk_save_objects(items)
    session.commit()
    session.close()
    return items


@dataclass
class Scraper(abc.ABC):
    """ Base class for Real Estate Scraper.
    """

    url: ClassVar[str]
    category_urls: ClassVar[List[str]]
    name: ClassVar[str] = field(init=False)

    def __post_init__(self):
        self.name = self.url.split("//")[-1].split("/")[0].split("?")[0]

    def scrape_all_items(self) -> List[RentProperty]:
        """ scrape and parse all items from starting url.
        """
        added = []
        for url in self.category_urls:
            while True:
                soup = make_request(url, soup=True)
                page_items = list(self.parse_page_items(soup))
                page_items = list(_filter_out_items_already_in_db(page_items))

                if not page_items:
                    break

                added += _add_items_to_db(page_items)
                url = self._next_page(soup)
                if not url:
                    break

        return added

    @staticmethod
    @abc.abstractmethod
    def _next_page(soup: BeautifulSoup) -> Optional[str]:
        """ Handle next page button to either continue or break the loop.
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
