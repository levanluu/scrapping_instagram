from anti_detect import AntiDetect
from context import Context
from http_client import HTTPClient
from proxy import Proxy


class BaseModel:
    """ Base Model """

    def __init__(
            self,
            http: HTTPClient = None,
            proxy: Proxy = None,
            anti_detect: AntiDetect = None,
            context: Context = None
    ):
        self._http = http
        self._proxy = proxy
        self._anti_detect = anti_detect
        self._context = context
