import os

from bs4 import BeautifulSoup

from http_requests.proxy import ProxyHandler
from http_requests.request import make_request

EXAMPLE = 'https://httpstat.us/'
EXAMPLE_200 = EXAMPLE + '200'
EXAMPLE_404 = EXAMPLE + '404'

IP_CHECK = 'https://api6.ipify.org/?format=json'
PROXY = os.path.join('tests', 'proxies.txt')
PROXY = ProxyHandler(PROXY).random_proxy

TEST_HEADERS = {
    "User-Agent": 'TEST AGENT'
}


class TestHTTP:
    def test_request_successful(self):
        response = make_request(EXAMPLE_200)
        assert response.status_code == 200

    def test_request_raise_incorrect_url_error(self):
        bad_url = 'google.com'
        try:
            make_request(bad_url)
            assert False
        except ValueError:
            assert True

    def test_request_404(self):
        response = make_request(EXAMPLE_404)
        assert response is None

    #
    # def test_request_use_proxy(self):
    #     response = make_request(IP_CHECK, proxies=PROXY)
    #     assert response.status_code == 200
    #     assert response.json()['ip'] == '192.227.241.117'

    def test_returns_soup(self):
        response = make_request(EXAMPLE_200, soup=True)
        assert type(response) is BeautifulSoup

    def test_custom_headers(self):
        response = make_request(EXAMPLE_200, headers=TEST_HEADERS)
        user_agent = response.request.headers['User-Agent']
        assert TEST_HEADERS['User-Agent'] == user_agent
