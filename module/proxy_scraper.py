import re
import ssl
import threading
import urllib.request
from time import sleep


def get_sourcecode(url):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request_source = urllib.request.urlopen(request).read()
        return str(request_source)

    except:
        return None


class ProxyScraper:

    def __init__(self, path_proxy_sources_file):
        self.proxies = set()  # ([ip:port, ...])
        self.path_proxy_sources_file = path_proxy_sources_file

    def scrape_proxy_source(self, url, socks=False):
        source = get_sourcecode(url)

        if source:
            re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}')
            re_proxy_reverse = re.compile('\d{1,6}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            replacements = {'&lt;': '<',
                            '&gt;': '>',
                            '</td><td>': ':',
                            '</a>': ':',
                            '::': ':',
                            ' ': ''}

            # modify sourcecode for regular expressions to be more successful
            for key in replacements:
                source = source.replace(key, replacements[key])

            proxies = re_proxy.findall(source)
            proxies_reverse = re_proxy_reverse.findall(source)

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
        proxy_sources = set()  # ([http://proxysite.com, ...])
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

            # guess if proxies scraped are SOCKS proxies
            if 'socks' in proxy_source:
                t = threading.Thread(target=self.scrape_proxy_source, args=[proxy_source], kwargs={'socks': True})

            else:
                t = threading.Thread(target=self.scrape_proxy_source, args=[proxy_source])

            thread_list.append(t)
            t.start()

        # wait for scraping to be finished before returning
        for t in thread_list:
            t.join()

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
