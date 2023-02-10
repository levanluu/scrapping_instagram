import asyncio
import logging
import json
from urllib.request import urlopen
from context import Context
from playwright.async_api import async_playwright
from fingerprint import stealth_async
from constants import ARGS


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


async def navigator(page):
    await page.add_init_script(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"deviceMemory",'
        '{get() {return 16}})'
    )
    await page.add_init_script(
        'Object.defineProperty('
        'Object.getPrototypeOf(navigator),'
        '"hardwareConcurrency",'
        '{get() {return 16}})'
    )


async def fingerprint(
        playwright,
        proxy: str = None,
):
    browser_type = playwright.webkit
    browser_device = playwright.devices["Desktop Chrome"]
    browser = await browser_type.launch(
        headless=False,
        args=ARGS,
        proxy={
            "server": "176.53.167.193:30011",
            "username": "quynh_nguyen+3_digitalf",
            "password": "ce0dd13d43"

        },
        devtools=False
    )

    timezone, lat, lon = get_timezone(proxy)
    geolocation = {'longitude': lon, 'latitude': lat} if lat and lon else None
    browser_context = await browser.new_context(
        locale='en-US, en',
        timezone_id=timezone,
        geolocation=geolocation,
        **browser_device
    )
    page = await browser_context.new_page()
    await stealth_async(page)
    await navigator(page)
    return page


async def main():
    async with async_playwright() as pw:
        page = await fingerprint(pw)
        await page.goto(
            url="https://browserleaks.com/canvas"
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
