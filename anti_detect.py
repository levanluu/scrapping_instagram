from http import HTTPClient


class AntiDetect:
    """ AntiDetect """

    def __init__(self):
        self._timezone = None
        self._latitude = None
        self._longitude = None

    def ip_info(self, html: str = None) -> None:
        self._timezone = html.get('timezone', None)
        self._latitude = html.get('lat', None)
        self._longitude = html.get('lon', None)

    def ip_detect(self) -> None:
        """ IP Info Detect """
        pass
