from .const import (auth_ssl, connection_timeout, header_items, header_items_cookies, home_url, login_url, post_data)
from requests import Session


class Browser:

    def __init__(self):
        self.combo = None
        self.proxy = None
        self.session = None
        self.auth_type = ''
        self.header = {}
        self.cookies = {}
        self.post_data = {}

    def create(self):
        self.session = Session()

        if auth_ssl:
            self.auth_type = 'https'
        else:
            self.auth_type = 'http'

    def initialize(self, combo, proxy):
        proxy_parts = proxy.split(':')
        proxy_ip = proxy_parts[0]
        proxy_port = proxy_parts[1]
        self.combo = combo
        self.proxy = {self.auth_type: self.auth_type + '://' + proxy_ip + ':' + proxy_port}
        self.session.proxies.update(self.proxy)

    def get_cookies(self):
        self.cookies = self.session.get(home_url, timeout=connection_timeout).cookies.get_dict()

    def set_header(self):
        if len(header_items_cookies):
            self.get_cookies()

        for header_cookie in header_items_cookies:
            if ';' in header_cookie:
                header_cookie_parts = header_cookie.split(';')
                
                if header_cookie_parts[1] in self.cookies:
                    self.header[header_cookie_parts[0]] = self.cookies[header_cookie_parts[1]]

        for header in header_items:
            if ';' in header:
                header_parts = header.split(';')
                self.header[header_parts[0]] = header_parts[1]

        self.session.headers.update(self.header)

    def set_post_data(self):
        username = self.combo[0]
        password = self.combo[1]
        for item in post_data:
            self.post_data[item] = post_data[item].format(username=username, password=password)

    def post(self):
        self.set_post_data()
        response = self.session.post(login_url, data=self.post_data, timeout=connection_timeout)
        return response
