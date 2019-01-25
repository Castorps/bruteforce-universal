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

    def scrape_proxies(self, url):
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
            self.proxies.update(proxies)

            # turn reversed format (port:ip) into normal format (ip:port)
            for proxy in proxies_reverse:
                proxy_parts = proxy.split(':')
                self.proxies.add(proxy_parts[1] + ':' + proxy_parts[0])

    def scrape(self):
        proxy_sources = set()  # ([http://proxysite.com, ...])

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

            t = threading.Thread(target=self.scrape_proxies, args=[proxy_source])
            t.start()

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
