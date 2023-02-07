import random
from typing import Union
from config import DEVICES
from constants import Device


class Context:
    """ Context Model """
    _DEVICES = DEVICES

    def __init__(self, is_mobile: bool = False):
        self.is_mobile: object = is_mobile

    def random_browser_context(self):
        if self.is_mobile:
            return self._DEVICES[Device.MOBILE.value][random.choice(list(Device.MOBILE)).value]
        return self._DEVICES[Device.DESKTOP.value][random.choice(list(Device.DESKTOP)).value]

    def get_browser_context(self, name: Union[Device.MOBILE, Device.DESKTOP] = None) -> dict:
        return self._DEVICES[Device.DESKTOP.value][name.value] \
            if isinstance(name, Device.MOBILE) \
            else self._DEVICES[Device.MOBILE.value][name.value]
