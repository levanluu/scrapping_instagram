import json
import logging

from http_client import HTTPClient


class AntiDetect(HTTPClient):
    """ AntiDetect """

    def __init__(self, proxy: str = None, headers: dict = None, *args, **kwargs):
        self.timezone = None
        self.latitude = None
        self.longitude = None
        self.country = None
        self.country_code = None
        self.region = None
        self.region_name = None
        self.city = None
        self.zipcode = None
        self.isp = None
        self.org = None
        self.real_ip = None
        super().__init__(proxy=proxy, headers=headers, *args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def ip_detect(self) -> bool:
        """ IP Info Detect """
        try:
            resp = self.http.request('GET', 'http://ip-api.com/json/')
            if resp.status == 200:
                html = json.loads(resp.data.decode('utf-8'))
                self.latitude = html.get('lat')
                self.longitude = html.get('lon')
                self.timezone = html.get('timezone')
                self.country = html.get('country')
                self.country_code = html.get('countryCode')
                self.region = html.get('region')
                self.region_name = html.get('regionName')
                self.city = html.get('city')
                self.zipcode = html.get('zip')
                self.isp = html.get('isp')
                self.org = html.get('org')
                self.real_ip = html.get('query')
                if self.proxy and self.real_ip in self._ip:
                    logging.info('Look good!')
                    return True
                elif self.proxy:
                    logging.warning('Look bad! Your ip is leaks.')

        except Exception as err:
            logging.error(err)
