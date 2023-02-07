import asyncio
import logging
import json
from urllib.request import urlopen
from context import Context
from playwright.async_api import async_playwright


def get_timezone(
        proxy: str = None
):

    url = f"http://ip-api.com/json/"
    if proxy:
        ip = proxy.split('//')
        ip = ip[1] if len(ip) > 1 else ip[0]
        ip = ip.split(':')[0] if ':' in ip else ip
        url = f"http://ip-api.com/json/{ip}"

    with urlopen(url) as resp:
        html = json.loads(resp.read().decode('utf-8'))
        timezone = html.get('timezone')
        lat = html.get('lat')
        lon = html.get('lon')

    return timezone, lat, lon


async def fingerprint(
        playwright,
        proxy: str = None,
):
    args = [
        "--start-maximized",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-web-security",
        "--disable-gpu",
        "--disable-gesture-requirement-for-media-playback",
        "--use-fake-codec-for-peer-connection",
        "--use-fake-device-for-media-stream",
        "--use-fake-mjpeg-decode-accelerator",
        "--use-fake-ui-for-fedcm",
        "--use-fake-ui-for-media-stream"
    ]
    if proxy:
        browser = await playwright.chromium.launch(
            headless=False,
            args=args,
            proxy=proxy,
            devtools=False,
            channel='chrome'
        )
    else:
        browser = await playwright.chromium.launch(
            headless=False,
            args=args,
            devtools=False,
            channel='chrome'
        )

    timezone, lat, lon = get_timezone(proxy)
    geolocation = {'longitude': lon, 'latitude': lat} if lat and lon else None
    context = Context(is_mobile=False).random_browser_context()
    browser_context = await browser.new_context(
        locale='en-US',
        user_agent=context['user-agent'],
        timezone_id=timezone,
        geolocation=geolocation,
        viewport=context['viewport'],
        extra_http_headers={'user-agent': context['user-agent']}
    )
    # Add script antidetect Browser
    # await browser_context.add_init_script(path='js/webgl.vendor.js')
    page = await browser_context.new_page()
    return page


async def main():
    async with async_playwright() as pw:
        page = await fingerprint(pw)
        await page.goto(
            url="https://bot.sannysoft.com/"
        )
        await asyncio.sleep(100000)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        logging.exception(e)
        loop.close()
