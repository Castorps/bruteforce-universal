from .const import (proxy_ban_time, proxy_minimum_attempts, proxy_success_ratio, proxy_timeout)
from collections import deque
from time import sleep, time


class ProxyManager:

    def __init__(self):
        self.proxies = {}  # {<ip>:<port>: [<status>, <tested>, <retries>, <disabled_timestamp>, <ban_flag>]}
        self.proxies_ready = deque()  # ([<ip>:port])
        self.isAlive = True

    @property
    def size(self):
        return len(self.proxies)

    def put(self, proxy_list):
        proxies_keys = list(self.proxies)
        for proxy in proxy_list:
            if proxy not in proxies_keys:
                self.proxies[proxy] = [0, 0, 0, None, False]
                self.proxies_ready.append(proxy)

    def get(self):
        return self.proxies_ready.popleft()

    def disable(self, proxy, tested=False, retries=False, ban_flag=False):
        proxy_stats = self.proxies[proxy]
        proxy_stats[0] = 2
        proxy_stats[3] = time()
        if tested:
            proxy_stats[1] += 1

        if retries:
            proxy_stats[2] += 1

        if ban_flag:
            proxy_stats[4] = True

        self.proxies[proxy] = [proxy_stats[0], proxy_stats[1], proxy_stats[2], proxy_stats[3], proxy_stats[4]]

    def stop(self):
        self.isAlive = False

    def start(self):
        while self.isAlive:
            for proxy in list(self.proxies):
                proxy_stats = self.proxies[proxy]

                if (proxy_stats[1] + proxy_stats[2]) >= proxy_minimum_attempts and proxy_stats[2] > 0:
                    proxy_ratio = round(proxy_stats[1] / proxy_stats[2], 2)

                    if proxy_ratio < proxy_success_ratio:
                        del self.proxies[proxy]

                if proxy_stats[3]:  # disabled?
                    if proxy_stats[4]:  # banned?
                        if (time() - proxy_stats[3]) >= proxy_ban_time:
                            self.proxies[proxy] = [0, proxy_stats[1], proxy_stats[2], None, False]
                            self.proxies_ready.append(proxy)
                    else:
                        if (time() - proxy_stats[3]) >= proxy_timeout:
                            self.proxies[proxy] = [0, proxy_stats[1], proxy_stats[2], None, False]
                            self.proxies_ready.append(proxy)

            sleep(0.5)
