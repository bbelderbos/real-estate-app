from bs4 import BeautifulSoup

from scrapers.morizon_scraper import (MorizonScraper,
                                      create_morizon_category_urls)
from scrapers.oto_dom_scraper import OtoDomScraper, create_otodom_category_urls
from tests._html import (MORIZON_ITEM_DETAIL_HTML, MORIZON_ITEMS_HTML,
                         OTODOM_ITEM_DETAIL_HTML, OTODOM_ITEMS_HTML)

OTODOM_CORRECT_ITEMS = BeautifulSoup(OTODOM_ITEMS_HTML, "html.parser")
OTODOM_CORRECT_ITEM = BeautifulSoup(OTODOM_ITEM_DETAIL_HTML, "html.parser")


def test_create_otodom_category_urls():
    lst = list(create_otodom_category_urls())
    assert len(lst) == 9


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
        assert data["title"] == "MARINA MOKOTÓW 3 pokoje Bezpośrednio"
        assert data["address"] == "Warszawa, Mokotów, Górny Mokotów"
        assert data["added_on"] is None
        assert data["area"] == 71
        assert type(data["area"]) is float
        assert data["level"] is None
        assert data["price"] == 3600.0
        assert type(data["price"]) is float
        assert data["rooms"] == 3
        assert type(data["rooms"]) is int
        assert data["offer_type"] == "Oferta prywatna"
        assert data["price_per_m"] is None
        assert data["site_id"] == "45757832"
        assert data["thumbnail_url"] is None
        assert (
            data["url"] == "https://www.otodom.pl/oferta/marina-mokotow-3-pokoje-"
            "bezposrednio-ID35ZHy.html#845e0b319d"
        )


MORIZON_CORRECT_ITEMS = BeautifulSoup(MORIZON_ITEMS_HTML, "html.parser")
MORIZON_CORRECT_ITEM = BeautifulSoup(MORIZON_ITEM_DETAIL_HTML, "html.parser")


def test_create_morizon_category_urls():
    lst = list(create_morizon_category_urls())
    assert len(lst) == 9


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
        assert data["title"] is None
        assert data["address"] == "Warszawa, Wilanów"
        assert data["added_on"] == "15-04-2020"
        assert data["area"] == 44
        assert type(data["area"]) is float
        assert data["level"] == "2/4"
        assert data["price"] == 2500.0
        assert type(data["price"]) is float
        assert data["rooms"] == 2
        assert type(data["rooms"]) is int
        assert data["price_per_m"] == "57,47 zł/m²"
        assert data["site_id"] == "mzn2036150919"
        assert data["thumbnail_url"] is None or data["thumbnail_url"].endswith(
            "thumbnail.jpg"
        )
        assert (
            data["url"]
            == "https://www.morizon.pl/oferta/wynajem-mieszkanie-warszawa-wilanow-43m2-mzn2036150919"
        )
        assert data["offer_type"] is None
