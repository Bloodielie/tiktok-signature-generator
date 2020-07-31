import asyncio
import random

from pyppeteer.launcher import Launcher

from .exceptions import TikTokBanned
from .stealth import stealth


class SignatureGenerator:
    def __init__(self) -> None:
        self.referrer = "https://www.tiktok.com/"

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.0 " \
                          "Safari/537.36) "

        self.options = {
            'args': [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certifcate-errors",
                "--ignore-certifcate-errors-spki-list",
                "--user-agent=" + self.user_agent
            ],
            'headless': True,
            'ignoreHTTPSErrors': True,
            'userDataDir': "./tmp",
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False,
            "autoClose": False
        }

        self._launcher = Launcher(options=self.options)
        self._browser = None
        self._initialization_lock = asyncio.Lock()
        self._verify_fp = None

    async def initialization(self):
        async with self._initialization_lock:
            if self._browser is None:
                self._browser = await self._create_browser()

            _context = await self._browser.createIncognitoBrowserContext()
            self._page = await _context.newPage()
            await self._page.emulate({
               'viewport': {'width': random.randint(320, 1920), 'height': random.randint(320, 1920), },
               'deviceScaleFactor': random.randint(1, 3),
               'isMobile': random.random() > 0.5,
               'hasTouch': random.random() > 0.5
            })
            await self._page.evaluateOnNewDocument("""() => {delete navigator.__proto__.webdriver;}""")
            await stealth(self._page)
            await self._page.goto("https://www.tiktok.com/@rihanna?lang=en", {
                'waitUntil': "load"
            })
            self.user_agent = await self._page.evaluate("""() => {return navigator.userAgent; }""")
            self._verify_fp = None

    async def _create_browser(self):
        return await self._launcher.launch()

    async def verify_fp(self):
        async with self._initialization_lock:
            if self._verify_fp is None:
                cookies: str = await self._page.evaluate('document.cookie;')
                if not cookies:
                    await self.close()
                    raise TikTokBanned("tick tok banned your ip")
                for text in cookies.replace(" ", "").split(";"):
                    try:
                        key, value = text.split("=")
                        if key == "s_v_web_id":
                            self._verify_fp = value
                            return value
                    except ValueError:
                        continue
            return self._verify_fp

    async def signature(self, url: str):
        verify_fp = await self.verify_fp()
        signature = await self._page.evaluate(
            '''() => {
                var url = "''' + url + "&verifyFp=" + verify_fp + '''"
                        var token = window.byted_acrawler.sign({url: url});
                        return token;
                    }''')
        return signature

    async def close(self):
        await self._page.close()
        await self._browser.close()
        await self._launcher.killChrome()
        self._browser.process.communicate()
