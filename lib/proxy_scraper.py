from sys import path
from time import time


class ProxyScraper:

    def __init__(self, input_proxy_file):
        self.proxies = set()
        self.proxy_file_path = input_proxy_file

    def scrape(self):
        proxies = []
        with open(self.proxy_file_path, 'r', encoding='utf-8', errors='ignore') as proxy_file:
            for proxy in proxy_file:
                    if ':' in proxy:
                        proxy = proxy.replace('\n', '').replace('\r', '').replace('\t', '')
                        proxies.append(proxy)

        self.proxies = set(proxies)

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
