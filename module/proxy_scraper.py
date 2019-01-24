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

    
def scrape_proxies(url):
    proxies = []
    proxies_reverse = []
    source = get_sourcecode(url)
    
    if source:
        re_proxy = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}')
        re_proxy_reverse = re.compile('\d{1,6}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        source = source.replace('&lt;', '<').replace('&gt;', '>').replace('</td><td>', ':').replace('</a>', ':').replace('::', ':')
        proxies = re_proxy.findall(source)
        proxies_reverse = re_proxy_reverse.findall(source)
        
        for proxy in proxies_reverse:
            proxy_parts = proxy.split(':')
            proxies += [proxy_parts[1] + ':' + proxy_parts[0]]

    return proxies


class ProxyScraper:

    def __init__(self):
        self.proxies = set()
        
    def scrape(self):
        proxies = []
        
        sslproxies_org = scrape_proxies('https://www.sslproxies.org/')
        freeproxylist_net = scrape_proxies('https://free-proxy-list.net/')
        freeproxylist_net_anon = scrape_proxies('https://free-proxy-list.net/anonymous-proxy.html')
        spys_me = scrape_proxies('http://spys.me/proxy.txt')

        proxies += (sslproxies_org
                   + freeproxylist_net
                   + freeproxylist_net_anon
                   + spys_me)

        self.proxies = set(proxies)

    def get(self):
        proxies = self.proxies
        self.proxies = set()
        return proxies
