from datetime import datetime

from bs4 import BeautifulSoup

from scrapers.morizon_scraper import (MorizonScraper,
                                      create_morizon_category_urls)
from scrapers.oto_dom_scraper import OtoDomScraper, create_otodom_category_urls
from tests._html import (MORIZON_ITEM_DETAIL_HTML, MORIZON_ITEMS_HTML,
                         OTODOM_ITEM_DETAIL_HTML, OTODOM_ITEMS_HTML)

MORIZON_CORRECT_ITEMS = BeautifulSoup(MORIZON_ITEMS_HTML, "html.parser")
MORIZON_CORRECT_ITEM = BeautifulSoup(MORIZON_ITEM_DETAIL_HTML, "html.parser")

OTODOM_CORRECT_ITEMS = BeautifulSoup(OTODOM_ITEMS_HTML, "html.parser")
OTODOM_CORRECT_ITEM = BeautifulSoup(OTODOM_ITEM_DETAIL_HTML, "html.parser")


def assert_rent_property_types(data):
    assert type(data["added_on"]) is datetime
    assert type(data["price"]) is int
    assert type(data["rooms"]) is int
    assert type(data["living_area"]) is float


class TestMorizonScraper:
    morizon = MorizonScraper()

    def test_ping(self):
        assert self.morizon.ping().status_code == 200

    def test_scrape_all_items(self):
        morizon = MorizonScraper()
        morizon.category_urls = [
            "https://www.morizon.pl/do-wynajecia/mieszkania/warszawa/stare-miasto/"
        ]
        items = morizon.scrape_all_items()
        assert len(items) > 35

    def test_parse_page_items_correct(self):
        data = list(self.morizon.parse_page_items(MORIZON_CORRECT_ITEMS))
        assert len(data) == 35

    def test_parse_preview_item_correct(self):
        data = self.morizon.parse_preview_item(MORIZON_CORRECT_ITEM)
        assert_rent_property_types(data)

        assert data["id"] == "mzn2036150919"
        assert data["source_site"] == "morizon.pl"
        assert data["title"] is data["address"]
        assert data["address"] == "Warszawa, Wilanów"
        assert data["added_on"].date() == datetime(year=2020, month=4, day=15).date()

        assert data["price"] == 250000
        assert data["rooms"] == 2
        assert data["living_area"] == 44

        assert (
            data["url"]
            == "https://www.morizon.pl/oferta/wynajem-mieszkanie-warszawa-wilanow-43m2-mzn2036150919"
        )

        assert data["thumbnail_url"] is None or data["thumbnail_url"].endswith(
            "thumbnail.jpg"
        )

        assert data["offer_type"] is None


class TestOtoDomScraper:
    otodom = OtoDomScraper()

    def test_ping(self):
        assert self.otodom.ping().status_code == 200

    def test_scrape_all_items(self):
        otodom = OtoDomScraper()
        otodom.category_urls = [
            "https://www.otodom.pl/wynajem/pokoj/warszawa/?nrAdsPerPage=72"
        ]
        items = otodom.scrape_all_items()
        assert len(items) > 72

    def test_parse_page_items_correct(self):
        data = list(self.otodom.parse_page_items(OTODOM_CORRECT_ITEMS))
        assert len(data) == 72

    def test_parse_preview_item_correct(self):
        data = self.otodom.parse_preview_item(OTODOM_CORRECT_ITEM.find("article"))
        assert_rent_property_types(data)

        assert data["id"] == "od45757832"
        assert data["source_site"] == "otodom.pl"
        assert data["title"] == "MARINA MOKOTÓW 3 pokoje Bezpośrednio"
        assert data["address"] == "Warszawa, Mokotów, Górny Mokotów"
        assert data["added_on"].date() == datetime.now().date()
        assert data["price"] == 360000
        assert data["rooms"] == 3
        assert data["living_area"] == 71
        assert (
            data["url"] == "https://www.otodom.pl/oferta/marina-mokotow-3-pokoje-"
            "bezposrednio-ID35ZHy.html#845e0b319d"
        )
        assert data["thumbnail_url"] is None  # TODO add thumbnail url
        assert data["private_offer"] is True


def test_create_morizon_category_urls():
    lst = list(create_morizon_category_urls())
    assert len(lst) == 9


def test_create_otodom_category_urls():
    lst = list(create_otodom_category_urls())
    assert len(lst) == 9
