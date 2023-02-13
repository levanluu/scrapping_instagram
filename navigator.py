from user_agent import UserAgent
from random import choice


class Navigator:
    def __init__(
            self,
            page: object = None,
            user_agent: str = None,
            locate: tuple = ("en-US", "vi"),
            concurrency: int = 8
    ):
        self.UserAgent: UserAgent = UserAgent(user_agent=user_agent)
        self.page = page
        self.languages = [locate[0], locate[1]]
        self.concurrency = concurrency

    async def loads(self) -> None:
        await self.UserAgent.loads(page=self.page)
        await self.device_memory()
        await self.hardware_concurrency()
        await self.language()

    async def device_memory(self) -> None:
        await self.page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator),'
            '"deviceMemory", {get() {return %s}})' % self.UserAgent.to_json(self.concurrency)
        )

    async def hardware_concurrency(self) -> None:
        await self.page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator),'
            '"hardwareConcurrency", {get() {return %s}})' % self.UserAgent.to_json(self.concurrency)
        )

    async def language(self) -> None:
        await self.page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator),'
            '"language", {get() {return %s}})' % self.UserAgent.to_json(self.languages[0])
        )
        await self.page.add_init_script(
            'Object.defineProperty(Object.getPrototypeOf(navigator),'
            '"languages", {get() {return %s}})' % self.UserAgent.to_json(self.languages)
        )
