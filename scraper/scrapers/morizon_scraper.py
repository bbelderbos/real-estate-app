""" Morizon.pl scraper class.
"""
from dataclasses import dataclass
from pprint import pprint
from typing import List, Generator

from bs4 import BeautifulSoup

from http_requests.request import make_request
from scrapers.scraper_base import Scraper

MORIZON_URL = 'https://morizon.pl'


def create_morizon_category_urls():
    """ Create category urls based on city, listing type and rent/sale.
    """
    for city in ['warszawa', 'poznan', 'wroclaw']:
        for listing_type in ['pokoje', 'mieszkania', 'domy']:
            for rent_sale in ['do-wynajecia']:
                yield f'{MORIZON_URL}/{rent_sale}/{listing_type}/najnowsze/{city}/'


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
                next_page = soup.find('a', {'title': 'następna strona'})
                if 'href' not in next_page.attrs.keys():
                    break
                url = self.url + next_page['href']
        pprint(items, indent=4)
        return items

    @staticmethod
    def parse_page_items(soup: BeautifulSoup) -> Generator[dict, None, None]:
        items = soup.find_all('div', {'class': 'row row--property-list'})[:-2]
        items = [MorizonScraper.parse_preview_item(x) for x in items]
        _ids = []
        for item in items:
            if item['site_id'] not in _ids:
                yield item
                _ids.append(item['site_id'])

    @staticmethod
    def parse_preview_item(soup: BeautifulSoup) -> dict:
        # print(soup.prettify())
        # input()
        address = soup.find('h2', {'class': 'single-result__title'}).text.strip()
        added_on = soup.find('span', {'class': 'single-result__category--date'}).text.strip()

        url = soup.find('a', {'itemprop': 'url'})['href']
        price = float(soup.find('meta', {'itemprop': 'price'})['content'])

        try:
            image = soup.find('meta', {'itemprop': 'image'})['content']
        except TypeError:
            image = None

        price_per_m = soup.find('p', {'class': 'single-result__price single-result__price--currency'}).text.strip()

        params = soup.find('ul', {'class': 'param list-unstyled list-inline'}).find_all('li')

        try:
            rooms = [int(x.find('b').text.strip()) for x in params
                     if any(c in x.text for c in ['pokoje', 'pokoi', 'pokój'])][0]
        except IndexError:
            rooms = None

        area = [float(x.find('b').text.replace(' ','').strip()) for x in params
                if 'm²' in x.text and 'działka' not in x.text][0]
        try:
            lot_area = [int(x.find('b').text.replace(' ','').strip()) for x in params
                        if 'działka' in x.text][0]
        except IndexError:
            lot_area = None

        try:
            level = [x.find('b').text.strip() for x in params if 'piętro' in x.text][0]
        except IndexError:
            level = None

        return {
            'title': None,
            'address': address,
            'added_on': added_on,
            'price': price,
            'rooms': rooms,
            'area': area,
            'lot_area': lot_area,
            'price_per_m': price_per_m,
            'level': level,
            'site_id': url[url.rfind('-')+1:],
            'url': url,
            'thumbnail_url': image,
            'offer_type': None
        }

    def parse_details_page(self, url: str):
        pass


# MorizonScraper().scrape_all_items()
