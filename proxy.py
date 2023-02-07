from constants import ProxyProtocol
from urllib3 import ProxyManager, make_headers
from urllib3.contrib.socks import SOCKSProxyManager


class Proxy:
    """ Proxy Model """

    def __init__(self, proxy: str, timeout: float = 3.0):
        self._proxy = proxy
        self._protocol = ProxyProtocol.HTTP.value
        self.__ip = None
        self.__port = None
        self.__username = None
        self.__password = None
        self._timeout = timeout

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
            self.__username, self.__password = auth.split(':')

        proxy = self._proxy.replace('/', '').split(':')
        proxy_len = len(proxy)
        if proxy_len == 5:
            self._protocol, self.__ip, self.__port, self.__username, self.__password = proxy
        elif proxy_len == 4:
            self.__ip, self.__port, self.__username, self.__password = proxy
        elif proxy_len == 3:
            self._protocol, self.__ip, self.__port = proxy
        elif proxy_len == 2:
            self.__ip, self.__port = proxy
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

        if self.__username and self.__password:
            return '{}://{}:{}@{}:{}'.format(self._protocol, self.__ip, self.__port, self.__username, self.__password)

        return '{}://{}:{}'.format(self._protocol, self.__ip, self.__port)

    @proxy_url.setter
    def proxy_url(self, value):
        self.__username, self.__password = None, None
        self._proxy = value

    def proxy_check(self) -> bool:
        proxy = ProxyManager(f"{self._protocol}://{self.__ip}:{self.__port}")
        if self._protocol.upper() == ProxyProtocol.SOCKS5.value:
            proxy = SOCKSProxyManager(f"{self._protocol}://{self.__ip}:{self.__port}")

        if self.__username and self.__password:
            headers = make_headers(proxy_basic_auth=f"{self.__username}:{self.__password}")
            proxy.proxy_headers = headers

        resp = proxy.request('GET', 'http://httpbin.org/ip')
        return True if resp.status == 200 else False
