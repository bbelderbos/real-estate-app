import os

from http_requests.proxy import ProxyHandler

PROXY = os.path.join('tests', 'proxies.txt')
EMPTY = os.path.join('tests', 'empty.txt')
with open(PROXY) as f:
    CORRECT_PROXIES = f.read().split('\n')


class TestProxy:

    def test_can_read_correct_txt_file(self):
        proxy_handler = ProxyHandler(PROXY)
        assert all(proxy in CORRECT_PROXIES for proxy in proxy_handler.proxies)
        assert len(proxy_handler.proxies) == 3

    def test_remove_duplicates(self):
        proxy_handler = ProxyHandler(PROXY)
        assert len(proxy_handler.proxies) == len(set(CORRECT_PROXIES))

    def test_raise_error_on_not_existing_file(self):
        try:
            ProxyHandler('not_exist.txt')
            assert False
        except FileNotFoundError:
            assert True

    def test_raise_error_on_empty_file(self):
        try:
            ProxyHandler(EMPTY)
            assert False
        except ValueError:
            assert True

    def test_random_proxy(self):
        proxy_handler = ProxyHandler(PROXY)
        random_proxy = proxy_handler.random_proxy
        assert any(random_proxy == proxy_handler.create_proxy_dict(proxy)
                   for proxy in proxy_handler.proxies)
