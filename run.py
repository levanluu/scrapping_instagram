import asyncio
import logging
import json
from urllib.request import urlopen
from context import Context
from playwright.async_api import async_playwright
from fingerprint import stealth_async
from constants import ARGS
from random import randint, uniform
from navigator import Navigator
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/110.0.0.0 Safari/537.36"
USERNAME = "bisdev001"
PASSWORD = "Abcd12345@"


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


async def login(page) -> None:
    await page.get_by_text("Phone number, username, or email").fill(USERNAME)
    await page.type('input[name="password"]', PASSWORD)
    await page.locator('button[type="submit"]').click()


async def fingerprint(
        playwright,
        proxy: str = None,
):
    browser_type = playwright.chromium
    browser_device = playwright.devices["Desktop Chrome"]
    browser_device["user_agent"] = USER_AGENT

    browser = await browser_type.launch(
        headless=False,
        args=ARGS,
        devtools=False
        # proxy={
        #     "server": "http://176.53.167.193:30011",
        #     "username": "quynh_nguyen+3_digitalf",
        #     "password": "ce0dd13d43"
        # }
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
    await Navigator(page=page, user_agent=USER_AGENT).loads()
    return page, browser_context


async def main():
    async with async_playwright() as pw:
        page, browser_context = await fingerprint(pw)

        # await page.goto(url="https://browserleaks.com/webrtc")
        # await asyncio.sleep(100)

        cookies = json.load(open('cookies/bisdev001_instagram_11-02-2023.json'))
        await page.context.add_cookies(cookies=cookies)
        await asyncio.sleep(3)
        await page.goto('https://www.instagram.com/')
        await page.wait_for_url('https://www.instagram.com/')
        with open('cookies/bisdev001_instagram_11-02-2023.json', 'w') as f:
            cookies = await page.context.cookies()
            json.dump(cookies, f, indent=4)
            print("Save cookies is ok!")
        friend_feed = []
        while len(friend_feed) < 50:
            if len(friend_feed) == 0:
                for i in range(5):
                    print(f"Auto-scroll => {i+1}")
                    await page.mouse.wheel(0, 900)
                    await asyncio.sleep(uniform(1, 3))
            else:
                for i in range(7):
                    print(f"Auto-scroll-second => {i+1}")
                    await page.mouse.wheel(0, 900)
                    await asyncio.sleep(uniform(1, 3))
            await asyncio.sleep(10)
            articles = await page.query_selector_all('article')
            for article in articles:
                try:
                    _ = await article.inner_html()
                    soup = BeautifulSoup(_, "html.parser")
                    tag_img = soup.find_all('img', {'class': 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'})
                    author = soup.select_one('div._aacl._aaco._aacw._aacx._aad6._aade')
                    content = soup.select_one(' h1._aacl._aaco._aacu._aacx._aad7._aade')
                    _aacl_aaco = soup.select_one(('div._aacl._aaco._aacw._aacx._aada._aade'))
                    image_url = []
                    for image in tag_img:
                        image_url.append(image['src'])
                    friend_feed_object = {'author': author.text, 'content': content.text, 'image_url': image_url, 'like': _aacl_aaco.text}
                    friend_feed.append(friend_feed_object)
                except:
                    continue
            print(len(friend_feed))
            print(friend_feed, '/////')
        await asyncio.sleep(100000)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        logging.exception(e)
        loop.close()
