import asyncio
import logging
import json
from urllib.request import urlopen
from playwright.async_api import async_playwright
from fingerprint import stealth_async
from constants import ARGS
from random import randint, uniform
from navigator import Navigator
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from ast import literal_eval

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/110.0.0.0 Safari/537.36"
USERNAME = "bisdev001"
PASSWORD = "Abcd12345@"
url = 'https://api.dev.socialeyez.io'

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
        getAuthProxies = None,
        getProxies = None
):
    print(getAuthProxies, '/////')
    browser_type = playwright.chromium
    browser_device = playwright.devices["Desktop Chrome"]
    browser_device["user_agent"] = getAuthProxies['userAgent']
    server = f"http://{getProxies['host']}:{getProxies['port']}"
    username = getProxies['username']
    password = getProxies['password']
    browser = await browser_type.launch(
        headless=True,
        args=ARGS,
        devtools=False,

        proxy={
            "server": server,
            "username": username,
            "password": password
        }
    )

    timezone, lat, lon = get_timezone(server)
    geolocation = {'longitude': lon, 'latitude': lat} if lat and lon else None
    browser_context = await browser.new_context(
        locale='en-US, en',
        timezone_id=timezone,
        geolocation=geolocation,
        **browser_device
    )
    page = await browser_context.new_page()
    await stealth_async(page)
    await Navigator(page=page, user_agent=getAuthProxies['userAgent']).loads()
    return page, browser_context


async def get_auth_social_networkByDate():
    today = datetime.now()
    print("Today's date:", today)
    authSocialNetwork = requests.get(url + f'/auth-social-network/auth_date?date=\"{today}\"&type=instagram')
    return authSocialNetwork.json()

async def update_auth_social_network(id_auth):
    headers = {"content-type": "application/json"}
    requests.put(url + f'/auth-social-network/{id_auth}/update', headers=headers)
    return

async def get_auth_proxies(id_auth):
    get_auth_proxies = requests.get(url + f'/auth-social-network/{id_auth}/get_auth_proxies').json()
    return get_auth_proxies

async def get_proxies(id_proxies):
    return requests.get(url + f'/proxies/{id_proxies}/findOne').json()

async def get_friend_list(id_auth):
    return requests.get(url + f'/friend-list/{id_auth}').json()

async def update_cookies_auth_social_network(auth_id, cookies):
    payload = json.dumps({
        "cookies": f'{cookies}'
    })
    headers = {
        'Content-Type': 'application/json'
    }
    url_update = f"{url}/auth-social-network/{auth_id}/update"

    response = requests.request("PUT", url_update, headers=headers, data=payload)
    return response.text

async def run():
    async with async_playwright() as pw:
        authSocialNetwork = await get_auth_social_networkByDate()
        if authSocialNetwork:
            await update_auth_social_network(authSocialNetwork['id'])
            getAuthProxies = await get_auth_proxies(authSocialNetwork['id'])
            if getAuthProxies:
                getProxies = await get_proxies(getAuthProxies['proxiesId'])
                print(getProxies)
                if getProxies:
                    page, browser_context = await fingerprint(pw, authSocialNetwork, getAuthProxies, getProxies)

                    # await page.goto(url="https://browserleaks.com/webrtc")
                    # await asyncio.sleep(100000)
                    cookies = literal_eval(authSocialNetwork['cookies'])
                    print(cookies)
                    await page.context.add_cookies(cookies=cookies)
                    await asyncio.sleep(3)
                    await page.goto('https://www.instagram.com/')
                    await page.wait_for_url('https://www.instagram.com/')
                    Arraycookies = await page.context.cookies()
                    await update_cookies_auth_social_network(authSocialNetwork['id'], Arraycookies)
                    print("Save cookies is ok!")
                    await asyncio.sleep(3)
                    await getFriendList(page, authSocialNetwork['id'])
                    await page.goto('https://www.instagram.com/')
                    await getFriendFeed(page, authSocialNetwork['id'])


async def getFriendList(page, auth_id):
    getFriendList = await get_friend_list(auth_id)

    if getFriendList == None:
        count_follower = 0
        friend_list = []
        await page.click('div.xh8yej3.x1iyjqo2 > div:nth-child(8)')
        await asyncio.sleep(5)
        tag_follower = await (await page.query_selector(
            'div.xh8yej3.x1gryazu.x10o80wk.x14k21rp.x1porb0y.x17snn68.x6osk4m > section > main > div > header > section > ul > li:nth-child(3)')).inner_text()
        if tag_follower:
            count_follower = tag_follower.split(' ')[0]
            headers = {"content-type": "application/json"}
            payloadSocialNetwork = json.dumps({
                "friends": count_follower,
            })
            requests.put(url + f'/auth-social-network/{auth_id}/update_social_network', headers=headers,
                         data=payloadSocialNetwork)

        await page.click('div.xh8yej3.x1gryazu.x10o80wk.x14k21rp.x1porb0y.x17snn68.x6osk4m > section > main > div > header > section > ul > li:nth-child(3)')
        await asyncio.sleep(3)
        await page.hover('div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano > div:nth-child(1) > div')
        for i in range(10):
            print(f"Auto-scroll => {i + 1}")
            await page.mouse.wheel(0, 900)
            await asyncio.sleep(uniform(3, 6))
        _aano = await page.query_selector('div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano > div:nth-child(1) > div')
        _ab8w = await _aano.query_selector_all('div.x9f619.x1n2onr6.x1ja2u2z.x1qjc9v5.x78zum5.xdt5ytf.x1iyjqo2.xl56j7k.xeuugli')

        for tag_friend in _ab8w:
            try:
                _html = await tag_friend.inner_html()
                soup = BeautifulSoup(_html, "html.parser")
                avatar = soup.select_one('img', {'class': 'x6umtig x1b1mbwd xaqea5y xav7gou xk390pu x5yr21d xpdipgo xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3'})['src']
                # _aano = soup.select_one('div', {'class': '_aano'})
                name = soup.select_one('div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x1iyjqo2.xs83m0k.xeuugli.x1qughib.x6s0dn4.x1a02dak.x1q0g3np.xdl72j9 > div > div > div:nth-child(1)').text
                link = f'https://www.instagram.com/{name}/'

                friend_list.append({ 'name': name, 'avatar': avatar, 'link': link, 'authSocialNetworkId': auth_id })
            except:
                print('error scraping data')
        if len(friend_list) > 0:
            try:
                payloadFriendList = json.dumps({
                    "payload": friend_list,
                })

                headers = {"content-type": "application/json"}
                response = requests.request("POST", url + "/friend-list/create-friend-list", headers=headers,
                                            data=payloadFriendList)
                print(response)
                return response
            except Exception as e:
                print('not found', e)

async def getFriendFeed(page, auth_id):
    friend_feed = []
    count_error = 0
    scroll_count = 0
    try:
        while len(friend_feed) < 50 and scroll_count < 100:
            if len(friend_feed) == 0:
                for i in range(5):
                    print(f"Auto-scroll => {i + 1}")
                    scroll_count +=1
                    await page.mouse.wheel(0, 900)
                    await asyncio.sleep(uniform(1, 3))
            else:
                for i in range(7):
                    print(f"Auto-scroll-second => {i + 1}")
                    await page.mouse.wheel(0, 900)
                    await asyncio.sleep(uniform(1, 3))
            await asyncio.sleep(10)
            articles = await page.query_selector_all('article')
            print(scroll_count, '/////')
            for article in articles:
                try:
                    _ = await article.inner_html()
                    soup = BeautifulSoup(_, "html.parser")
                    tag_img = soup.find_all('img', {'class': 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'})
                    _aaqt = soup.select_one('div', { 'class': '_aaqt' })
                    author = _aaqt.select_one('div > div._aasi._aasj._ai9a > div > header > div._aaqy._aaq- > div._aar0._aar1 > div:nth-child(1) > div > div > span > div')
                    content = soup.select_one('h1', { 'class': '_aacl _aaco _aacu _aacx _aad7 _aade' })
                    # _aacl_aaco = soup.select_one(('div._aacl._aaco._aacw._aacx._aada._aade'))
                    image_url = []
                    for image in tag_img:
                        image_url.append(image['src'])
                    friend_feed_object = {'author': author.text, 'content': content.text, 'urls_images': image_url}
                    friend_feed.append(friend_feed_object)
                except:
                    print('error ')
                    continue
            print(len(friend_feed))
    except:
        print('error scraping data')

    await page.close()

    if len(friend_feed) > 0:
         try:
             payloadFriendFeed = json.dumps({
                 "authSocialNetworkId": auth_id,
                 "payload": friend_feed,
             })
             headers = {"content-type": "application/json"}
             response = requests.request("POST", url + "/scraping-friend-feed/store/instagram", headers=headers, data=payloadFriendFeed)
             print(response)
             return response
         except Exception as e:
             print('not found', e)
async def main():
    while True:
        authSocialNetwork = await get_auth_social_networkByDate()
        if authSocialNetwork:
            await run()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        logging.exception(e)
        loop.close()