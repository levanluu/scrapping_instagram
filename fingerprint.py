import json
from dataclasses import dataclass
from typing import Tuple, Optional, Dict

from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


def from_file(name):
    """read script from /js data directory"""
    with open(f'./json/fingerprint/{name}', 'r') as f:
        return f.read()


SCRIPTS: Dict[str, str] = {
    'chrome_app': from_file('chrome.app.js'),
    'chrome_csi': from_file('chrome.csi.js'),
    'chrome_load_times': from_file('chrome.load_times.js'),
    'chrome_runtime': from_file('chrome.runtime.js'),
    'fingerprint': from_file('fingerprint.js'),
    'hairline': from_file('hairline.js'),
    'iframe_content_window': from_file('iframe.contentWindow.js'),
    'magic-arrays': from_file('magic-arrays.js'),
    'media_codecs': from_file('media.codecs.js'),
    'navigator_hardware_concurrency': from_file('navigator.hardwareConcurrency.js'),
    'navigator_languages': from_file('navigator.languages.js'),
    'navigator_permissions': from_file('navigator.permissions.js'),
    'navigator_platform': from_file('navigator.platform.js'),
    'navigator_plugins': from_file('navigator.plugins.js'),
    'navigator_user_agent': from_file('navigator.userAgent.js'),
    'navigator_vendor': from_file('navigator.vendor.js'),
    'outer_dimensions': from_file('window.outer_dimensions.js'),
    'user_agent_data': from_file('navigator.user_agent_data.js'),
    'utils': from_file('utils.js'),
    'webdriver': from_file('navigator.webdriver.js'),
    'webgl_vendor': from_file('webgl.vendor.js'),
    'webrtc': from_file('webrtc.js'),
}


@dataclass
class StealthConfig:
    """
    Playwright Stealth Configuration that applies stealth strategies to Playwright Page objects.

    The stealth strategies are contained in /js package and are basic javascript scripts that are executed
    on every Page.goto call.

    Note:
        All init scripts are combined by playwright into one script and then executed this means
        the scripts should not have conflicting constants/variables etc. !
        This also means scripts can be extended by overriding enabled_scripts generator:

        ```
        @property
        def enabled_scripts():
            yield 'console.log("first script")'
            yield from super().enabled_scripts()
            yield 'console.log("last script")'
        ```
    """
    # scripts
    chrome_app: bool = True
    chrome_csi: bool = True
    chrome_load_times: bool = True
    chrome_runtime: bool = True
    fingerprint: bool = True
    hairline: bool = True
    iframe_content_window: bool = True
    media_codecs: bool = True
    navigator_hardware_concurrency: int = 8
    navigator_languages: bool = True
    navigator_permissions: bool = True
    navigator_platform: bool = True
    navigator_plugins: bool = True
    navigator_user_agent: bool = True
    navigator_vendor: bool = True
    outer_dimensions: bool = True
    user_agent_data = True
    webdriver: bool = True
    webgl_vendor: bool = True
    webrtc: bool = True

    # options
    vendor: str = 'Intel Inc.'
    renderer: str = 'Intel Iris OpenGL Engine'
    nav_vendor: str = 'Google Inc.'
    nav_user_agent: Optional[str] = None
    nav_platform: Optional[str] = None
    languages: Tuple[str] = ('en-US', 'en')
    run_on_insecure_origins: Optional[bool] = None

    @property
    def enabled_scripts(self):
        opts = json.dumps({
            'webgl_vendor': self.vendor,
            'webgl_renderer': self.renderer,
            'navigator_vendor': self.nav_vendor,
            'navigator_platform': self.nav_platform,
            'navigator_user_agent': self.nav_user_agent,
            'languages': list(self.languages),
            'runOnInsecureOrigins': self.run_on_insecure_origins,
            'hardwareConcurrency': self.navigator_hardware_concurrency,
            'userAgentData': self.user_agent_data,
        })
        # defined options constant
        yield f'const opts = {opts}'
        # init utils and magic-arrays helper
        yield SCRIPTS['utils']
        yield SCRIPTS['magic-arrays']

        if self.webdriver:
            yield SCRIPTS['webdriver']
        if self.outer_dimensions:
            yield SCRIPTS['outer_dimensions']
        if self.webgl_vendor:
            yield SCRIPTS['webgl_vendor']
        if self.navigator_vendor:
            yield SCRIPTS['navigator_vendor']
        if self.navigator_plugins:
            yield SCRIPTS['navigator_plugins']
        if self.navigator_permissions:
            yield SCRIPTS['navigator_permissions']
        if self.navigator_languages:
            yield SCRIPTS['navigator_languages']
        # if self.navigator_platform:
        #     yield SCRIPTS['navigator_platform']
        # if self.navigator_user_agent:
        #     yield SCRIPTS['navigator_user_agent']
        if self.media_codecs:
            yield SCRIPTS['media_codecs']
        if self.iframe_content_window:
            yield SCRIPTS['iframe_content_window']
        if self.chrome_runtime:
            yield SCRIPTS['chrome_runtime']
        if self.chrome_load_times:
            yield SCRIPTS['chrome_load_times']
        if self.chrome_csi:
            yield SCRIPTS['chrome_csi']
        if self.chrome_app:
            yield SCRIPTS['chrome_app']
        if self.hairline:
            yield SCRIPTS['hairline']
        if self.webrtc:
            yield SCRIPTS['webrtc']
        # if self.fingerprint:
        #     yield SCRIPTS['fingerprint']
        # if self.user_agent_data:
        #     yield SCRIPTS['user_agent_data']


def stealth_sync(page: SyncPage, config: StealthConfig = None):
    """teaches synchronous playwright Page to be stealthy like a ninja!"""
    for script in (config or StealthConfig()).enabled_scripts:
        page.add_init_script(script)


async def stealth_async(page: AsyncPage, config: StealthConfig = None):
    """teaches asynchronous playwright Page to be stealthy like a ninja!"""
    for script in (config or StealthConfig()).enabled_scripts:
        await page.add_init_script(script)
