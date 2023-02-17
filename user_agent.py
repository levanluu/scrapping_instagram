import json

from user_agents import parse


class UserAgent:
    def __init__(self, user_agent: str = None):
        self.user_agent = user_agent
        self.ua = parse(self.user_agent)

    @property
    def platform(self):
        if "mac" == self.ua.device.family.lower() and "intel" in self.user_agent.lower():
            return "MacIntel"
        return self.ua.os.family

    @property
    def app_version(self):
        if 'firefox' in self.user_agent.lower():
            app_version = self.user_agent.split(";")[0]
            app_version = app_version.split("/")[1]
            return f"{app_version})"
        return self.user_agent.split("/")[1]

    @property
    def app_code_name(self):
        return self.user_agent.split("/")[0]

    @property
    def user_agent_data(self):
        brand = "Chromium" if "chrome" in self.ua.browser.family.lower() else self.ua.browser.family
        version = str(self.ua.browser.version[0])
        return {
            'brands': [
                {"brand": brand, "version": version},
                {"brand": "Not A(Brand", "version": "24"},
                {"brand": self.ua.browser.family, "version": version},
            ],
            "mobile": self.is_mobile,
            "platform": "macOS" if "mac" in self.ua.os.family.lower() else self.ua.os.family
        }

    @property
    def cpu(self):
        cpu = self.user_agent.split(";")[1].strip().split()
        return cpu[0].strip()

    @property
    def os(self):
        return self.ua.os.family

    @property
    def os_version(self):
        return None

    @property
    def version(self):
        return self.ua.os.version_string

    @property
    def oscpu(self):
        return None

    @property
    def is_mobile(self):
        return self.ua.is_mobile

    @staticmethod
    def to_json(obj):
        return json.dumps(obj)

    async def loads(self, page) -> None:
        await self.load_user_agent_data(page=page)
        await self.load_platform(page=page)
        await self.load_app_code_name(page=page)
        await self.load_app_version(page=page)
        # await self.load_oscpu(page=page)

    async def load_user_agent_data(self, page) -> None:
        await page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator), '
            '"userAgentData", {get() {return %s}})' % self.to_json(self.user_agent_data)
        )

    async def load_platform(self, page) -> None:
        await page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator), '
            '"platform", {get() {return %s}})' % self.to_json(self.platform)
        )

    async def load_app_code_name(self, page) -> None:
        await page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator), '
            '"appCodeName", {get() {return %s}})' % self.to_json(self.app_code_name)
        )

    async def load_app_version(self, page) -> None:
        if self.ua.os.version:
            await page.add_init_script(
                'Object.defineProperty(Object.getPrototypeOf(navigator), '
                '"appVersion", {get() {return %s}})' % self.to_json(self.app_version)
            )

    async def load_oscpu(self, page) -> None:
        await page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator), '
            '"oscpu", {get() {return %s}})' % self.to_json(self.oscpu)
        )
