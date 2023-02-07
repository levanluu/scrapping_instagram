import logging
from typing import Any

from urllib3 import PoolManager, ProxyManager, make_headers
from urllib3.contrib.socks import SOCKSProxyManager

import json
from constants import ProxyProtocol
from proxy import Proxy


class HTTPClient(Proxy):
    """ HTTP Client """

    def __init__(self, url: str, proxy: str = None, headers: dict = None, *args, **kwargs):
        self.url = url
        self.proxy = proxy
        self.headers = headers
        self.status_code = None
        self.response = None
        super().__init__(proxy=proxy)

    def get(self):
        return self.request_handle('GET')

    def post(self):
        return self.request_handle('POST')

    def request_handle(self, method: str = 'GET'):
        try:
            resp = self.http.request(method, self.url)
            if resp.status == 200:
                return json.loads(resp.data.decode('utf-8'))

        except Exception as err:
            logging.error(err)

        return ConnectionError

    @property
    def http(self) -> Any:
        http = PoolManager(headers=self.headers)
        if self._protocol.upper() == ProxyProtocol.SOCKS5.value:
            http = SOCKSProxyManager(f"{self._protocol}://{self._ip}:{self._port}", headers=self.headers)
        elif self.proxy:
            http = ProxyManager(f"{self._protocol}://{self._ip}:{self._port}", headers=self.headers)

        if self.proxy and self._username and self._password:
            headers = make_headers(proxy_basic_auth=f"{self._username}:{self._password}")
            http.proxy_headers = headers

        return http
