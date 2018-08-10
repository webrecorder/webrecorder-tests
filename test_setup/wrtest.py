from asyncio import AbstractEventLoop
from typing import ClassVar, Optional, Dict, Tuple
from typing import Union

import pytest
from async_timeout import timeout
from grappa import should, expect
from grappa.api import TestProxy
from selenium.webdriver.remote.webdriver import WebDriver
from simplechrome import Page, Frame

from .constants import Waits, WAITS

__all__ = ["WRAutoTestTimeOut", "WRTest", "WRSeleniumTest", "WRSimpleChromeTest"]


class WRAutoTestTimeOut(Exception):
    """Class to indicate an auto-test did not run complete within a time limit"""


class WRTest(object):
    """Base Webrecorder Test class. Home to utilities used by all tests"""

    test_type: ClassVar[str] = "WRTest"
    should: ClassVar[TestProxy] = should  # Should style assertions
    expect: ClassVar[TestProxy] = expect  # Expect style assertions
    manifest: ClassVar[str] = ""  # Path to manifest to be used by the test
    preinject: ClassVar[bool] = False  # JavaScript injection particular
    test_to: Union[int, float] = 30  # how long to wait for each js function to resolve
    url: str = ""
    js: str = ""
    player: Tuple[str, str, str] = None
    pywb_url: str = ""
    chrome_opts: Dict[str, str] = {}


@pytest.mark.autowired
class WRSeleniumTest(WRTest):
    """Base Test Class For Browsers Controlled Using Selenium"""

    test_type: ClassVar[str] = "Selenium"
    FRAME_LOAD: ClassVar[
        str
    ] = """
    var cb = arguments[arguments.length - 1];
    if (document.readyState === "complete") cb();
    var to = setInterval(function () {
      if (document.readyState === "complete") {
        clearInterval(to);
        cb();
      }
    }, 1000);
    """
    driver: WebDriver = None

    def test_all(self, test_name: str) -> None:
        self.driver.get(self.url)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wb_iframe"))
        self.driver.execute_async_script(self.FRAME_LOAD)
        to_inject = f"""
        var cb = arguments[arguments.length - 1];
        {self.js}
        Promise.resolve().then(() => {test_name}()).then(cb).catch(() => cb(false));
        """
        self.driver.execute_async_script(to_inject) | self.should.be.true


@pytest.mark.autowired
class WRSimpleChromeTest(WRTest):
    """Base Test Class For Browsers Controlled Using Simplechrome"""

    test_type: ClassVar[str] = "Simplechrome"
    preinject: ClassVar[bool] = True  # JavaScript injection particular
    waits: ClassVar[Waits] = WAITS
    page: ClassVar[Page] = None
    loop: ClassVar[AbstractEventLoop] = None

    async def goto_test(self, wait: Optional[Dict[str, str]] = None) -> Frame:
        """
        Navigate the browser to the test page.
        Optionally waiting for a specific browser event.

        :param wait: Optional wait for event to happen
        :type wait: WAITS
        :return: The frame containing the replayed page
        :rtype: simplechrome.Frame
        """
        await self.page.goto(self.url, self.waits.dom_load)
        replay_frame = self.page.frames[1]
        replay_frame.enable_lifecycle_emitting()
        await replay_frame.navigation_waiter(loop=self.loop, timeout=5)
        if wait is not None:
            if wait == self.waits.load:
                await replay_frame.loaded_waiter(loop=self.loop, timeout=15)
            elif wait == self.waits.net_idle:
                await replay_frame.network_idle_waiter(loop=self.loop, timeout=15)
        return replay_frame

    @pytest.mark.asyncio
    async def test_all(self, test_name: str) -> None:
        """Default test method, called once per each test listed in the manifest"""
        replay_frame = await self.goto_test(self.waits.load)
        async with timeout(self.test_to) as to:
            results = await replay_frame.evaluate(f"{test_name}()")
        if to.expired:
            raise WRAutoTestTimeOut(
                f"{test_name} did not resolve within {self.test_to} seconds"
            )
        results | self.should.be.true
