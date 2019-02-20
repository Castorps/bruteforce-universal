import re
import ssl
import threading
import urllib.request
from time import sleep
from sys import path


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
def get_path_separator():
    if 'linux' in platform or 'darwin' in platform:
        return '/'
    elif 'win' in platform:
        return '\\'
    else:
        return '/'
class ProxyScraper:

    def __init__(self, path_proxy_sources_file):
        self.proxies = set()  # ([ip:port, ...])
        self.path_proxy_sources_file = path_proxy_sources_file
        self.proxy_source_stats = {}

    def scrape_url(self, url, socks=False):
        re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}')
        re_proxy_reverse = re.compile('\d{1,6}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        source = get_sourcecode(url)
        proxy_count = 0
        if source:

            replacements = {' ': '',
                            '&lt;': '<',
                            '&gt;': '>',
                            '</td><td>': ':',
                            '</a>': ':',
                            '", "': ':',
                            '","PORT":"': ':',
                            ',"': ':',
                            ':::': ':',
                            '::': ':'}

            # modify sourcecode so regular expressions can scrape more
            for key in replacements:
                source = source.replace(key, replacements[key])

            proxies = re_proxy.findall(source)
            proxies_reverse = re_proxy_reverse.findall(source)
            proxy_count += len(proxies)
            proxy_count += len(proxies_reverse)
            self.proxy_source_stats[url] = proxy_count

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
        self.proxy_source_stats = {}
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

            if 'socks' in proxy_source:
                t = threading.Thread(target=self.scrape_url, args=[proxy_source], kwargs={'socks': True})

            else:
                t = threading.Thread(target=self.scrape_url, args=[proxy_source])

            thread_list.append(t)
            t.start()

        # wait for scraping to be finished before returning to main thread
        for t in thread_list:
            t.join()

        proxy_source_stats_file = open(path[0] + get_path_separator() + 'proxy_sources_stats.txt', 'w+',
                                       encoding='utf-8', errors='ignore')

        for proxy_source in self.proxy_source_stats:
            proxy_source_stats_file.write(proxy_source + ' : ' + str(self.proxy_source_stats[proxy_source]) + '\n')

        proxy_source_stats_file.close()

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
