from .const import (auth_ssl, connection_timeout, headers, headers_cookies, home_url, login_url, payload)
from requests import Session


class Browser:

    def __init__(self):
        self.session = None
        self.combo = None
        self.cookies = {}
        self.payload = {}
        self.auth_type = None

    def create(self):
        self.session = Session()

        if auth_ssl:
            self.auth_type = 'https'
        else:
            self.auth_type = 'http'

    def set_details(self, combo, proxy):
        self.combo = combo

        if not proxy[2] or not proxy[3]:
            proxy_auth = ''
        else:
            proxy_auth = proxy[2] + ':' + proxy[3] + '@'

        proxy = {self.auth_type: proxy[1] + '://' + proxy_auth + proxy[0]}
        self.session.proxies.update(proxy)

    def get_cookies(self):
        self.cookies = self.session.get(home_url, timeout=connection_timeout).cookies.get_dict()

    def set_header(self):
        if len(headers_cookies):
            self.get_cookies()

        for header_name, cookie_name in headers_cookies.items():
            if cookie_name in self.cookies:
                headers[header_name] = self.cookies[cookie_name]

        self.session.headers.update(headers)

    def build_payload(self):
        for field in payload:
            self.payload[field] = payload[field].format(username=self.combo[0], password=self.combo[1])

    def post(self):
        response = self.session.post(login_url, data=self.payload, timeout=connection_timeout)
        return response
