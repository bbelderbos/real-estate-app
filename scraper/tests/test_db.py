from datetime import datetime

from data.db_session import DbSession
from data.rent_property import RentProperty


class TestDbSession:
    def test_db_global_init(self):
        assert DbSession.engine is None
        assert DbSession.factory is None

        DbSession.global_init()

        assert DbSession.engine is not None
        assert DbSession.factory is not None

    def test_db_already_init(self):
        assert DbSession.global_init() is False


DATE = datetime.now()

CORRECT_RENT_PROPERTY = {
    "id": "od-12324556",
    "source_site": "otodom.pl",
    "title": "ladne mieszkanie na mokotowie",
    "address": "Mokotow, Warszawa",
    "added_on": DATE,
    "price": 140000,
    "rooms": 2,
    "living_area": 56.0,
    "url": "https://otodom.pl/example-rent-listing",
    "thumbnail_url": "https://otodom.pl/thumbnail.jpg",
    "private_offer": True,
}


class TestDbModels:
    def test_create_rent_property(self):
        rent_property = RentProperty(**CORRECT_RENT_PROPERTY)
        assert rent_property.id == CORRECT_RENT_PROPERTY["id"]
        assert rent_property.source_site == CORRECT_RENT_PROPERTY["source_site"]
        assert rent_property.title == CORRECT_RENT_PROPERTY["title"]
        assert rent_property.address == CORRECT_RENT_PROPERTY["address"]
        assert rent_property.added_on == CORRECT_RENT_PROPERTY["added_on"]
        assert rent_property.price == CORRECT_RENT_PROPERTY["price"]
        assert rent_property.rooms == CORRECT_RENT_PROPERTY["rooms"]
        assert rent_property.living_area == CORRECT_RENT_PROPERTY["living_area"]
        assert rent_property.url == CORRECT_RENT_PROPERTY["url"]
        assert rent_property.thumbnail_url == CORRECT_RENT_PROPERTY["thumbnail_url"]
        assert rent_property.private_offer == CORRECT_RENT_PROPERTY["private_offer"]
