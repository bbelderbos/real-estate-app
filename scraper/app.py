from time import sleep
from datetime import datetime

from data.db_session import DbSession
from scrapers.morizon_scraper import MorizonScraper
from scrapers.oto_dom_scraper import OtoDomScraper


def main():
    print(len(MorizonScraper().scrape_all_items()), 'added from morizon.pl')
    print(len(OtoDomScraper().scrape_all_items()), 'added from otodom.pl')


if __name__ == '__main__':
    DbSession.global_init()
    while True:
        print(f"[{datetime.now()}] scraping")
        main()
        sleep(360)
        break
