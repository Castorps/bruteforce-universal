import re
import ssl
import threading
import urllib.request
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlparse
from datetime import datetime
from html.parser import unescape


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
        r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'})
        r_source = urllib.request.urlopen(r)
        r_source_read = str(r_source.read())
        return unescape(r_source_read)
    except:
        return None


class ProxyScraper:

    def __init__(self, path_proxy_sources_file, path_proxy_sources_log_file):
        self.proxies = {}  # ([ip:port:type:username:password, ...]; ip:port mandatory)
        self.proxy_source_log = {}  # {url: number_of_proxies_collected, ...}
        self.path_proxy_sources_file = path_proxy_sources_file
        self.path_proxy_sources_log_file = path_proxy_sources_log_file

    def add_proxy(self, proxy, proxy_type=None):
        if proxy in self.proxies:
            if not self.proxies[proxy] and proxy_type:
                self.proxies[proxy] = proxy_type
        else:
            self.proxies[proxy] = proxy_type

    def scrape_website(self, url, depth=0, origin=None):
        re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}')
        re_proxy_reverse = re.compile('\d{2,5}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        proxy_count = 0

        if depth < 3 and url not in self.proxy_source_log:
            source = get_sourcecode(url)
        else:
            source = None

        if not origin:
            origin = url

        if source:
            soup = BeautifulSoup(source, 'html.parser')
            links = soup.find_all('a', href=True) + string_between(source, '<link>', '</link>')
            url_parse = urlparse(url)
            date_year = datetime.now().year

            replacements = {
                '\n': ':',
                '\t': ':',
                '\r': ':',
                '<td>': ':',
                '</td>': ':',
                '<a>': ':',
                '</a>': ':',
                '"': ':',
                "'": ':',
                ',': ':',
                'ip': ':',
                'port': ':',
                'type': ':',
                'country': ':',
                'proxy': ':',
                'prx': ':',
                '</': ':',
                '<': ':',
                '>': ':'
            }

            source = source.lower()  # makes parsing simpler (e.g. PORT == port)
            source = re.sub(' +', ':', source)  # replace multiple whitespaces with ':'

            # modify sourcecode so regular expressions can scrape more
            for key in replacements:
                source = source.replace(key, replacements[key])

            source = re.sub(':+', ':', source)  # replace multiple ':' with just one
            proxies = re_proxy.findall(source)
            proxies_reverse = re_proxy_reverse.findall(source)

            # update proxy counter
            proxy_count += len(proxies)
            proxy_count += len(proxies_reverse)

            if origin in self.proxy_source_log:
                proxy_count += self.proxy_source_log[origin]

            self.proxy_source_log[origin] = proxy_count

            for proxy in proxies:
                if 'socks' in origin:
                    self.add_proxy(proxy, proxy_type='socks5')
                else:
                    self.add_proxy(proxy)

            # turn reversed format (port:ip) into normal format (ip:port)
            for proxy in proxies_reverse:
                proxy_parts = proxy.split(':')
                proxy = proxy_parts[1] + ':' + proxy_parts[0]

                if 'socks' in origin:
                    self.add_proxy(proxy, proxy_type='socks5')
                else:
                    self.add_proxy(proxy)

            # get all links that are likely to contain proxies
            for link in links:

                try:
                    link_url = str(link['href'])
                except (KeyError, TypeError):
                    link_url = link

                link_url_parse = urlparse(link_url)

                if not link_url_parse.scheme and not link_url_parse.netloc:
                    link_url = url_parse.scheme + '://' + url_parse.netloc + link_url

                elif not link_url_parse.scheme and link_url_parse.netloc:
                    link_url = url_parse.scheme + '://' + link_url.replace('://', '')
                    link_url = link_url.replace('////', '//')

                if (url_parse.netloc in link_url and
                        ('/p/' in link_url or '/' + str(date_year) + '/' in link_url)):

                    self.scrape_website(link_url, depth=depth + 1, origin=origin)

        return

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
            while threading.active_count() >= 10:
                sleep(0.5)

            t = threading.Thread(target=self.scrape_website, args=[proxy_source])
            t.start()
            thread_list.append(t)

        # wait for scraping sources to be finished
        for t in thread_list:
            t.join()

        # log how many proxies each proxy source provided
        with open(self.path_proxy_sources_log_file, 'w+', encoding='utf-8', errors='ignore') as proxy_source_log_file:
            for proxy_source in sorted(self.proxy_source_log):
                proxy_source_log_file.write(proxy_source + ' ; ' + str(self.proxy_source_log[proxy_source]) + '\n')

    def get(self):
        proxies = []

        for proxy in self.proxies:
            proxy_type = self.proxies[proxy]

            if proxy_type:
                proxies.append(proxy + ':' + self.proxies[proxy])
            else:
                proxies.append(proxy)

        self.proxies = {}
        return proxies
