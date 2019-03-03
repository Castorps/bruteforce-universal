from .const import (auth_ssl, connection_timeout, headers, headers_cookies, home_url, login_url, payload, payload_json, payload_put)
from requests import Session
from json import dumps


class Browser:

    def __init__(self):
        self.session = None
        self.combo = None
        self.cookies = {}  # {cookie_name: cookie_value, ...}
        self.payload = {}  # {payload_field: payload_value, ...}
        self.auth_type = None

    def create_session(self):
        self.session = Session()

        if auth_ssl:
            self.auth_type = 'https'
        else:
            self.auth_type = 'http'

    def set_details(self, combo, proxy):
        self.combo = combo

        # set authentication by look at username and password of proxy
        if not proxy[2] or not proxy[3]:
            proxy_auth = ''
        else:
            proxy_auth = proxy[2] + ':' + proxy[3] + '@'

        proxy = {self.auth_type: proxy[1] + '://' + proxy_auth + proxy[0]}
        self.session.proxies.update(proxy)

    def get_cookies(self):
        self.cookies = self.session.get(home_url, timeout=connection_timeout).cookies.get_dict()

    def set_header(self):
        if len(home_url):
            self.get_cookies()

        # include cookie values in header (=dictionary)
        for header_name, cookie_name in headers_cookies.items():
            if cookie_name in self.cookies:
                headers[header_name] = self.cookies[cookie_name]

        # build_payload has to be called first, if payload is supposed to be json
        for field in headers:
            headers[field] = headers[field].format(content_length=str(len(self.payload)))

        self.session.headers.update(headers)

    def build_payload(self):
        for field in payload:
            self.payload[field] = str(payload[field]).format(username=self.combo[0], password=self.combo[1])

        if payload_json:
            self.payload = dumps(self.payload).encode('utf-8')

    def post(self):
        if payload_put:
            response = self.session.put(login_url, data=self.payload, timeout=connection_timeout)
        else:
            response = self.session.post(login_url, data=self.payload, timeout=connection_timeout)
        return response
