from constants import ProxyProtocol


class Proxy:
    """ Proxy Model """

    def __init__(self, proxy: str, timeout: float = 3.0, http=None):
        self._proxy = proxy
        self._protocol = ProxyProtocol.HTTP.value
        self._ip = None
        self._port = None
        self._username = None
        self._password = None
        self._timeout = timeout
        self._http = http

    def __repr__(self):
        return self.proxy_url

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._proxy = self._proxy.replace(self._protocol, value)
        self._protocol = value

    @property
    def proxy_url(self) -> str:
        if '@' in self._proxy:
            self._proxy, auth = self._proxy.split('@')
            self._username, self._password = auth.split(':')

        proxy = self._proxy.replace('/', '').split(':')
        proxy_len = len(proxy)
        if proxy_len == 5:
            self._protocol, self._ip, self._port, self._username, self._password = proxy
        elif proxy_len == 4:
            self._ip, self._port, self._username, self._password = proxy
        elif proxy_len == 3:
            self._protocol, self._ip, self._port = proxy
        elif proxy_len == 2:
            self._ip, self._port = proxy
        else:
            raise ValueError("""
                Wrong formatter, support protocol [http, https, socks5], None is http.
                Usage:
                     socks5://127.0.0.1:8000
                     socks5://127.0.0.1:8000@username:password
                     socks5://127.0.0.1:8000:username:password
                     127.0.0.1:8000@username:password
                     127.0.0.1:8000:username:password
                """)

        if self._protocol.upper() not in ProxyProtocol.__members__.keys():
            raise ValueError('We only support protocol: HTTP, HTTPS & SOCK5')

        if self._username and self._password:
            return '{}://{}:{}@{}:{}'.format(self._protocol, self._ip, self._port, self._username, self._password)

        return '{}://{}:{}'.format(self._protocol, self._ip, self._port)

    @proxy_url.setter
    def proxy_url(self, value):
        self._username, self._password = None, None
        self._proxy = value

    def proxy_check(self) -> bool:
        resp = self._http.request('GET', 'http://httpbin.org/ip')
        return True if resp.status == 200 else False
