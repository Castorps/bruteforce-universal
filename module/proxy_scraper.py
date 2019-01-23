import re
import ssl
import urllib.request


def get_sourcecode(url):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request_source = urllib.request.urlopen(request).read()
        return str(request_source)
    
    except:
        return None

    
def scrape_table_proxies(url):
    proxies = []
    source = get_sourcecode(url)
    
    if source:
        re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}')
        source = source.replace('</td><td>', ':')
        proxies = re_proxy.findall(source)

    return proxies


class ProxyScraper:

    def __init__(self):
        self.proxies = set()
        
    def scrape(self):
        proxies = []
        
        sslproxies_org = scrape_table_proxies('https://www.sslproxies.org/')
        freeproxylist_net = scrape_table_proxies('https://free-proxy-list.net/')
        freeproxylist_net_anon = scrape_table_proxies('https://free-proxy-list.net/anonymous-proxy.html')
        spys_me = scrape_table_proxies('http://spys.me/proxy.txt')

        proxies += (sslproxies_org
                   + freeproxylist_net
                   + freeproxylist_net_anon
                   + spys_me)

        self.proxies = set(proxies)

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
