""" Morizon.pl scraper class.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from pprint import pprint
from typing import Generator, List

from bs4 import BeautifulSoup

from http_requests.request import make_request
from scrapers.scraperbase import Scraper

MORIZON_URL = "https://morizon.pl"


def create_morizon_category_urls():
    """ Create category urls based on city, listing type and rent/sale.
    """
    for city in ["warszawa", "poznan", "wroclaw"]:
        for listing_type in ["pokoje", "mieszkania", "domy"]:
            for rent_sale in ["do-wynajecia"]:
                yield f"{MORIZON_URL}/{rent_sale}/{listing_type}/najnowsze/{city}/"


@dataclass
class MorizonScraper(Scraper):
    """ morizon.pl scraper class.
    """

    url = MORIZON_URL
    category_urls = create_morizon_category_urls()

    def scrape_all_items(self) -> List[dict]:
        items = []
        for url in self.category_urls:
            while True:
                soup = make_request(url, soup=True)
                items += list(self.parse_page_items(soup))
                next_page = soup.find("a", {"title": "następna strona"})
                if "href" not in next_page.attrs.keys():
                    break
                url = self.url + next_page["href"]
        pprint(items, indent=4)
        return items

    def parse_page_items(self, soup: BeautifulSoup) -> Generator[dict, None, None]:
        items = soup.find_all("div", {"class": "row row--property-list"})[:-2]
        items = [self.parse_preview_item(x) for x in items]
        _ids = []
        for item in items:
            if item["id"] not in _ids:
                yield item
                _ids.append(item["id"])

    def parse_preview_item(self, soup: BeautifulSoup) -> dict:
        address = soup.find("h2", {"class": "single-result__title"}).text.strip()
        added_on = soup.find(
            "span", {"class": "single-result__category--date"}
        ).text.strip()

        title = address

        if added_on == "dzisiaj":
            added_on = datetime.now()
        elif added_on == "wczoraj":
            added_on = datetime.now() - timedelta(days=1)
        else:
            added_on = datetime.strptime(added_on, "%d-%m-%Y")

        url = soup.find("a", {"itemprop": "url"})["href"]

        idx = url.rfind("-") + 1
        _id = url[idx:]

        # Convert price to grosze (cents)
        price = int(float(soup.find("meta", {"itemprop": "price"})["content"]) * 100)

        try:
            image = soup.find("meta", {"itemprop": "image"})["content"]
        except TypeError:
            image = None

        params = soup.find("ul", {"class": "param list-unstyled list-inline"}).find_all(
            "li"
        )

        try:
            rooms = [
                int(x.find("b").text.strip())
                for x in params
                if any(c in x.text for c in ["pokoje", "pokoi", "pokój"])
            ][0]
        except IndexError:
            rooms = None

        area = [
            float(x.find("b").text.replace(" ", "").strip())
            for x in params
            if "m²" in x.text and "działka" not in x.text
        ][0]
        try:
            lot_area = [
                int(x.find("b").text.replace(" ", "").strip())
                for x in params
                if "działka" in x.text
            ][0]
        except IndexError:
            lot_area = None

        return {
            "title": title,
            "address": address,
            "added_on": added_on,
            "price": price,
            "rooms": rooms,
            "living_area": area,
            "lot_area": lot_area,
            "id": _id,
            "url": url,
            "thumbnail_url": image,
            "offer_type": None,
            "source_site": self.name,
        }

    def parse_details_page(self, url: str):
        pass
