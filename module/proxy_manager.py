from .const import (proxy_ban_time, proxy_minimum_attempts, proxy_success_ratio, proxy_timeout)
from collections import deque
from threading import Thread
from time import (sleep, time)


class ProxyManager:

    def __init__(self):
        self.proxies = {}  # see below; holds all proxies and there parameters
        self.proxies_ready = deque()  # see below; holds ready proxies and authentication parameters
        self.maintain_thread = None
        self.isAlive = True

    @property
    def size(self):
        return len(self.proxies)

    def put(self, proxy_list):
        
        # add proxies from proxy_list ([ip:port:type:username:password, ...]; ip:port mandatory) to self.proxies
        # parse ip, port, type, username, password
        for proxy in proxy_list:
            proxy_parts = proxy.split(':')
            proxy_ip = proxy_parts[0]
            proxy_port = proxy_parts[1]

            if len(proxy_parts) == 2:
                proxy_type = 'http'
                proxy_username = None
                proxy_password = None

            if 2 < len(proxy_parts) < 5:
                proxy_type = proxy_parts[2]
                proxy_username = None
                proxy_password = None

            if len(proxy_parts) >= 5:
                proxy_type = proxy_parts[2]
                proxy_username = proxy_parts[3]
                proxy_password = proxy_parts[4]

            proxy_type = proxy_type.lower()
                
            if proxy_type not in ['http', 'socks5', 'socks5h']:
                proxy_type = 'http' 

            self.proxies[proxy_ip + ':' + proxy_port] = [proxy_type,  # type
                                                         proxy_username,  # username
                                                         proxy_password,   # password
                                                         0,   # tested
                                                         0,   # retries
                                                         None,   # disabled timestamp
                                                         False]  # ban flag

            # add proxy to pool of 'ready' proxies if it's not in there already
            if [proxy_ip + ':' + proxy_port, proxy_type, proxy_username, proxy_password] not in self.proxies_ready:
                self.proxies_ready.append([proxy_ip + ':' + proxy_port,
                                           proxy_type,
                                           proxy_username,
                                           proxy_password])

    def get(self):
        while not len(self.proxies_ready) and self.isAlive:
            sleep(0.5)
            
        return self.proxies_ready.popleft()

    def disable(self, proxy, tested=False, retries=False, ban_flag=False):
        try:
            proxy_stats = self.proxies[proxy[0]]
            proxy_stats[5] = time()

            if tested:
                proxy_stats[3] += 1

            if retries:
                proxy_stats[4] += 1

            if ban_flag:
                proxy_stats[6] = True

        except KeyError:
            return

    def maintain(self):
        while self.isAlive:

            # list avoids changing dictionary during loop
            for proxy in list(self.proxies):
                proxy_stats = self.proxies[proxy]

                # calculate proxy success ratio and delete it if it's too bad
                if (proxy_stats[3] + proxy_stats[4]) >= proxy_minimum_attempts and proxy_stats[4] > 0:
                    proxy_ratio = proxy_stats[3] / proxy_stats[4]

                    if proxy_ratio < proxy_success_ratio:
                        del self.proxies[proxy]
                        continue

                if proxy_stats[5]:

                    # banned or disabled? => set wait time
                    if proxy_stats[6]:
                        time_limit = proxy_ban_time

                    else:
                        time_limit = proxy_timeout

                    # enable proxy if wait time has passed
                    if (time() - proxy_stats[5]) >= time_limit:
                        proxy_stats[5] = None
                        proxy_stats[6] = False

                        self.proxies_ready.append([proxy,
                                                   proxy_stats[0],
                                                   proxy_stats[1],
                                                   proxy_stats[2]])

            sleep(0.5)

    def stop(self):
        self.isAlive = False
        self.maintain_thread.join()

    def start(self):
        self.isAlive = True
        self.maintain_thread = Thread(target=self.maintain)
        self.maintain_thread.start()
