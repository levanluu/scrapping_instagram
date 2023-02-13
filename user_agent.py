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
            app_version = app_version.split("/")
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
            "mobile": self.ua.is_mobile,
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
        return f"{self.ua.os.version[0]}.{self.ua.os.version[1]}"

    @property
    def version(self):
        return self.ua.os.version_string

    @property
    def os_cpu(self):
        return f"{self.cpu} {self.os} {self.os_version}"
