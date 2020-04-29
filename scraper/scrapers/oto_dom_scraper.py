""" Otodom.pl scraper class.
"""
from pprint import pprint
from typing import Generator, List

from bs4 import BeautifulSoup

from http_requests.request import make_request
from scrapers.scraper_base import Scraper

OTODOM_URL = 'https://otodom.pl'


def create_otodom_category_urls():
    for region in ['mazowieckie', 'malopolskie', 'dolnoslaskie']:
        for _type in ['wynajem']:
            for property_type in ['mieszkanie', 'dom', 'pokoj']:
                yield f'{OTODOM_URL}/{_type}/{property_type}/{region}/?nrAdsPerPage=72'


class OtoDomScraper(Scraper):
    url = OTODOM_URL
    category_urls = create_otodom_category_urls()

    def scrape_all_items(self) -> List[dict]:
        items = []
        for url in self.category_urls:
            while True:
                soup = make_request(url, soup=True)
                items += list(self.parse_page_items(soup))
                next_page = soup.find('a', {'data-dir': 'next'})
                if 'disabled' in next_page['class']:
                    break
                url = next_page['href']
                print(url)
        pprint(items, indent=4)
        return items

    @staticmethod
    def parse_page_items(soup: BeautifulSoup) -> Generator[dict, None, None]:
        items = soup.find_all('article', {'class': 'offer-item',
                                          'data-featured-name': 'listing_no_promo'})
        return [OtoDomScraper.parse_preview_item(x) for x in items]

    @staticmethod
    def parse_preview_item(soup: BeautifulSoup) -> dict:
        _id = soup['data-tracking-id']
        title = soup.find('span', {'class': 'offer-item-title'}).text.strip()
        address = soup.find('p', {'class': 'text-nowrap'})
        address.find('span').extract()
        address = address.text.strip()

        rooms = soup.find('li', {'class': 'offer-item-rooms'})
        if rooms:
            rooms = int(rooms.text.split(' ')[0])

        area = soup.find('li', {'class': 'offer-item-area'})
        if area:
            area = area.text.replace('m²', '').replace(',', '.').strip()
            area_dict = {
                'jednoosobowy': 1,
                'dwuosobowy': 2,
                'trzyosobowy i więcej': 3
            }
            if area in area_dict.keys() and rooms is None:
                rooms = area_dict[area]
            else:
                area = float(area)


        price = float(soup.find('li', {'class': 'offer-item-price'}).text
                      .replace('/mc', '').replace('zł', '')
                      .replace(' ', '').replace(',', '.').strip())
        offer_type = soup.find('li', {'class': 'pull-right'}).text.strip()
        return {
            'title': title,
            'address': address,
            'added_on': None,
            'area': area,
            'rooms': rooms,
            'price': price,
            'offer_type': offer_type,
            'level': None,
            'price_per_m': None,
            'site_id': _id,
            'thumbnail_url': None,
            'url': soup['data-url']

        }

    def parse_details_page(self, url: str):
        pass
