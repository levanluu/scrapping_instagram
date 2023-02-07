from enum import Enum


class MobileDevice(Enum):
    """ List of Mobile Devices """

    SAMSUNG_GALAXY_S22 = 'SAMSUNG_GALAXY_S22'
    SAMSUNG_GALAXY_S21 = 'SAMSUNG_GALAXY_S21'
    IPHONE_13_PRO_MAX = 'IPHONE_13_PRO_MAX'
    APPLE_12 = 'APPLE_12'
    APPLE_IPHONE_XS = 'APPLE_IPHONE_XS'


class DesktopDevice(Enum):
    """ List of Desktop Devices """

    MACOS = 'MACOS'
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'


class Device:
    """ List of Devices """

    MOBILE = MobileDevice
    DESKTOP = DesktopDevice


class ProxyProtocol(Enum):
    HTTP = 'http'
    HTTPS = 'https'
    SOCKS5 = 'socks5'
