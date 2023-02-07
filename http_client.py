from urllib3 import PoolManager, ProxyManager, make_headers
from urllib3.contrib.socks import SOCKSProxyManager

from constants import ProxyProtocol
from proxy import Proxy


class HTTPClient(Proxy):
    """ HTTP Client """

    def __init__(self, proxy: str = None, headers: dict = None, *args, **kwargs):
        self.proxy = proxy
        self.headers = headers
        super().__init__(proxy=proxy)

    @property
    def http(self) -> PoolManager | ProxyManager | SOCKSProxyManager:
        http = PoolManager(headers=self.headers)
        if self._protocol.upper() == ProxyProtocol.SOCKS5.value:
            http = SOCKSProxyManager(f"{self._protocol}://{self._ip}:{self._port}", headers=self.headers)
        elif self.proxy:
            http = ProxyManager(f"{self._protocol}://{self._ip}:{self._port}", headers=self.headers)

        if self.proxy and self._username and self._password:
            headers = make_headers(proxy_basic_auth=f"{self._username}:{self._password}")
            http.proxy_headers = headers

        return http
