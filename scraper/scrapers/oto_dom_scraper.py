""" Otodom.pl scraper.
"""
from datetime import datetime
from typing import Generator, Optional

from bs4 import BeautifulSoup

from scrapers.scraperbase import Scraper

OTODOM_URL = "https://otodom.pl"


def create_otodom_category_urls():
    for region in ["warszawa"]:  # , "malopolskie", "dolnoslaskie"]:
        for _type in ["wynajem"]:
            for property_type in ["mieszkanie"]:  # , "dom", "pokoj"]:
                yield f"{OTODOM_URL}/{_type}/{property_type}/{region}/?nrAdsPerPage=72"


class OtoDomScraper(Scraper):
    """ Otodom.pl scraping class.
    """
    url = OTODOM_URL
    category_urls = create_otodom_category_urls()

    @staticmethod
    def _next_page(soup: BeautifulSoup) -> Optional[str]:
        next_page = soup.find("a", {"data-dir": "next"})
        if "disabled" in next_page["class"]:
            return None
        return next_page["href"]

    def parse_page_items(self, soup: BeautifulSoup) -> Generator[dict, None, None]:
        items = soup.find_all(
            "article", {"class": "offer-item", "data-featured-name": "listing_no_promo"}
        )
        for item in items:
            yield self.parse_preview_item(item)

    def parse_preview_item(self, soup: BeautifulSoup) -> dict:
        _id = soup["data-tracking-id"]
        title = soup.find("span", {"class": "offer-item-title"}).text.strip()
        address = soup.find("p", {"class": "text-nowrap"})
        address.find("span").extract()
        address = address.text.strip()

        rooms = soup.find("li", {"class": "offer-item-rooms"})
        if rooms:
            rooms = int(rooms.text.split(" ")[0].replace(">", ''))

        area = soup.find("li", {"class": "offer-item-area"})
        if area:
            area = area.text.replace("m²", "").replace(",", ".").strip()
            area_dict = {"jednoosobowy": 1, "dwuosobowy": 2, "trzyosobowy i więcej": 3}
            if area in area_dict.keys() and rooms is None:
                rooms = area_dict[area]
                area = None
            else:
                area = float(area.replace(' ', ''))

        price = int(
            float(
                soup.find("li", {"class": "offer-item-price"})
                    .text.replace("/mc", "")
                    .replace("zł", "")
                    .replace(" ", "")
                    .replace(",", ".")
                    .replace('~', '')
                    .strip()
            )
            * 100
        )
        offer_type = soup.find("li", {"class": "pull-right"}).text.strip()
        return {
            "title": title,
            "address": address,
            "added_on": datetime.now(),
            "living_area": area,
            "rooms": rooms,
            "price": price,
            "private_offer": True if offer_type == "Oferta prywatna" else False,
            "id": "od" + _id,
            "thumbnail_url": None,
            "url": soup["data-url"],
            "source_site": self.name,
        }

    def parse_details_page(self, url: str):
        pass
