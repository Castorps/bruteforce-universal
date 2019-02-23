import re
import ssl
import threading
import urllib.request
from time import sleep


def string_between(string_input, string_leading, string_trailing):
    matches = []
    occurrence = 0

    while True:
        try:
            string_leading_index = string_input.index(string_leading, occurrence)
            string_trailing_index = string_input.index(string_trailing, string_leading_index + len(string_leading))
            string_match = string_input[string_leading_index + len(string_leading): string_trailing_index]
            matches.append(string_match)
            occurrence = string_trailing_index

        except ValueError:
            return matches


def get_sourcecode(url):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request_source = urllib.request.urlopen(request).read()
        return str(request_source)

    except:
        return None


class ProxyScraper:

    def __init__(self, path_proxy_sources_file, path_proxy_sources_log_file):
        self.proxies = set()  # ([ip:port:type:username:password, ...]; ip:port mandatory)
        self.proxy_source_log = {}  # {url: number_of_proxies_collected, ...}
        self.path_proxy_sources_file = path_proxy_sources_file
        self.path_proxy_sources_log_file = path_proxy_sources_log_file

    def scrape_website(self, url, socks=False):
        re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}')
        re_proxy_reverse = re.compile('\d{2,5}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        source = get_sourcecode(url)
        proxy_count = 0

        if source:

            replacements = {'&lt;': '<',
                            '&gt;': '>',
                            '</td><td>': ':',
                            '</a>': ':',
                            '"': ':',
                            ',': ':',
                            'IP': ':',
                            'PORT': ':'}

            source = re.sub(' +', ':', source)  # replace multiple whitespaces with ':'

            # modify sourcecode so regular expressions can scrape more
            for key in replacements:
                source = source.replace(key, replacements[key])

            source = re.sub(':+', ':', source)  # replace multiple ':' with just one
            proxies = re_proxy.findall(source)
            proxies_reverse = re_proxy_reverse.findall(source)

            # keep track of how many proxies each proxy source provided
            proxy_count += len(proxies)
            proxy_count += len(proxies_reverse)

            if url in self.proxy_source_log:
                proxy_count += self.proxy_source_log[url]

            self.proxy_source_log[url] = proxy_count

            for proxy in proxies:
                if socks:
                    proxy += ':socks5'

                self.proxies.add(proxy)

            # turn reversed format (port:ip) into normal format (ip:port)
            for proxy in proxies_reverse:
                proxy_parts = proxy.split(':')
                proxy = proxy_parts[1] + ':' + proxy_parts[0]

                if socks:
                    proxy += ':socks5'

                self.proxies.add(proxy)

    def scrape(self):
        self.proxy_source_log = {}
        proxy_sources = set()
        thread_list = []

        # load proxy sources
        with open(self.path_proxy_sources_file, 'r', encoding='utf-8', errors='ignore') as proxy_sources_file:
            for line in proxy_sources_file:
                if '://' in line:
                    proxy_source = line.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    proxy_sources.add(proxy_source)

        # scrape proxy sources
        for proxy_source in proxy_sources:
            while threading.active_count() > 10:
                sleep(0.5)

            # scrape multiple sites simultaneously; guess if source provides socks proxies or not
            if 'socks' in proxy_source:
                t = threading.Thread(target=self.scrape_website, args=[proxy_source], kwargs={'socks': True})

            else:
                t = threading.Thread(target=self.scrape_website, args=[proxy_source])

            t.start()
            thread_list.append(t)

        # wait for scraping to be finished before returning to main thread
        for t in thread_list:
            t.join()

        # log how many proxies each proxy source provided
        with open(self.path_proxy_sources_log_file, 'w+', encoding='utf-8', errors='ignore') as proxy_source_log_file:
            for proxy_source in sorted(self.proxy_source_log):
                proxy_source_log_file.write(proxy_source + ': ' + str(self.proxy_source_log[proxy_source]) + '\n')

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
