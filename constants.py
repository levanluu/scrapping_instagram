from enum import Enum

ARGS = [
    "--autoplay-policy=user-gesture-required",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-update",
    "--disable-default-apps",
    "--disable-dev-shm-usage",
    "--disable-domain-reliability",
    "--disable-features=AudioServiceOutOfProcess",
    "--disable-gesture-requirement-for-media-playback",
    "--disable-hang-monitor",
    "--disable-ipc-flooding-protection",
    "--disable-notifications",
    "--disable-offer-store-unmasked-wallet-cards",
    "--disable-popup-blocking",
    "--disable-print-preview",
    "--disable-prompt-on-repost",
    "--disable-renderer-backgrounding",
    "--disable-setuid-sandbox",
    "--disable-speech-api",
    "--disable-sync",
    "--disable-web-security",
    "--disk-cache-size=33554432",
    "--hide-scrollbars",
    "--ignore-gpu-blocklist",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-default-browser-check",
    "--no-first-run",
    "--no-pings",
    "--no-sandbox",
    "--no-zygote",
    "--password-store=basic",
    "--start-maximized",
    "--use-fake-codec-for-peer-connection",
    "--use-fake-mjpeg-decode-accelerator",
    "--use-fake-ui-for-fedcm",
    "--use-fake-ui-for-media-stream",
    "--use-mock-keychain"
]


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

    MOBILE = 'MOBILE'
    DESKTOP = 'DESKTOP'


class ProxyProtocol(Enum):
    HTTP = 'http'
    HTTPS = 'https'
    SOCKS5 = 'socks5'
