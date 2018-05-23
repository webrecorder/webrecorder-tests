import asyncio
from typing import (Any, Awaitable, Dict, Optional)
from pyppeteer import launch as _launch
from pyppeteer.frame_manager import Frame
from pyppeteer.browser import Browser, Page
from pyppeteer.network_manager import Response


def merge_dict(dict1: Optional[Dict], dict2: Optional[Dict]) -> Dict:
    new_dict = {}
    if dict1:
        new_dict.update(dict1)
    if dict2:
        new_dict.update(dict2)
    return new_dict


class TestBrowser(object):
    """
    Convenience wrapper around pyppeteer
    """

    def __init__(self, browser_exec: Optional[str] = None, headless: Optional[bool] = True) -> None:
        self.headless: bool = headless
        self.launched_browser: bool = False
        self.browser_exec: Optional[str] = browser_exec
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.top: Optional[Frame] = None  # actual top frame
        self.replay_frame: Optional[Frame] = None  # replay_iframe

    async def launch(self) -> None:
        launch_args = dict(
            executablePath=self.browser_exec,
            headless=self.headless,
        )
        self.browser = await _launch(launch_args)
        self.page = await self.browser.newPage()
        self.launched_browser = True

    async def _rif_did_nav(self) -> None:
        """
        Resolves when the replay_iframe has navigated.
        This method can only be used one the browser has navigated to archive_top otherwise
        this will resolve on that frames navigation event.

        Emulates the JS node.js implementation below but using asyncio.Events
            async function waitForNav(page) {
              let done;
              const prom = new Promise((resolve) => done = resolve));
              page.once('framenavigated', done);
              await prom;
            }
        """
        event = asyncio.Event()

        # TODO(n0tan3rd): fix this for prime time, this is hack
        def wait(frame: Frame) -> None:
            if 'mp_' in frame.url:
                event.set()

        self.page.once('framenavigated', wait)
        return await event.wait()

    def _rif_did_load(self) -> Awaitable:
        """
        Returns an future that will resolve once replay_iframe's documents readyState is complete.
        The function polled checks for for the following condition to be true `document.readyState === "complete"`
        """
        task = self.replay_frame.waitForFunction(
            '() => document.readyState === "complete"',
            polling=100
        )
        return asyncio.ensure_future(task)

    async def goto(self, url: str, options: Optional[Dict[str, str]] = None, **kwargs: Any) -> Optional[Response]:
        """
        If the remote browser was not launched yet launch it.
        Got to page and await the top frame wait condition to be resolved
        Wait for the replay_iframe to navigate and load
        """
        if not self.launched_browser:
            await self.launch()
        if options is None:
            options = {'waitUntil': 'networkidle0'}
        opts = merge_dict(options, kwargs)
        res = await self.page.goto(url, opts)
        await self._rif_did_nav()
        self.top = self.page.mainFrame
        self.replay_frame = self.top.childFrames[0]
        await self._rif_did_load()
        return res

    async def replay_eval(self, js: str) -> Any:
        result = await self.replay_frame.evaluate(js)
        return result

    async def close(self) -> None:
        await self.browser.close()

    async def eval_on_new_document(self, page_function: str, *args: str) -> None:
        """Evaluate a function on every new document"""
        return await self.page.evaluateOnNewDocument(pageFunction=page_function, *args)

    @property
    def top_url(self) -> str:
        """Get the url of archive top"""
        return self.top.url

    async def top_title(self) -> str:
        """Get the document title of archive top"""
        return await self.top.title()

    @property
    def replay_url(self) -> str:
        """Get the url of the page within replay_iframe"""
        return self.replay_frame.url

    async def replay_title(self) -> str:
        """Get the document title of the page within replay_iframe"""
        return await self.replay_frame.title()


async def create(browser_exec: Optional[str] = None, headless: bool = False) -> TestBrowser:
    tb = TestBrowser(browser_exec, headless)
    await tb.launch()
    return tb
