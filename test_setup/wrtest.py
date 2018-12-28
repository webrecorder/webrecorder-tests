from asyncio import AbstractEventLoop

from selenium.webdriver.remote.webdriver import WebDriver
from simplechrome import Page, Frame, NavigationTimeoutError
from typing import ClassVar, Dict, Tuple
from typing import Union

from .constants import Waits, WAITS

__all__ = ["WRAutoTestTimeOut", "WRTest", "BaseSimpleChromeTest", "BaseWRSeleniumTest"]


class WRAutoTestTimeOut(Exception):
    """Class to indicate an auto-test did not run complete within a time limit"""


class WRTest(object):
    """Base Webrecorder Test class. Home to utilities used by all tests"""

    test_type: ClassVar[str] = "WRTest"
    manifest: ClassVar[str] = ""  # Path to manifest to be used by the test
    preinject: ClassVar[bool] = False  # JavaScript injection particular
    test_to: Union[int, float] = 60  # how long to wait for each js function to resolve
    url: str = ""
    js: str = ""
    player: Tuple[str, str, str] = None
    pywb_url: str = ""
    chrome_opts: Dict[str, str] = {}


class BaseWRSeleniumTest(WRTest):
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

    def goto_test(self) -> None:
        self.driver.get(self.url)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wb_iframe"))
        self.driver.execute_async_script(self.FRAME_LOAD)


class BaseSimpleChromeTest(WRTest):
    """Base Test Class For Browsers Controlled Using Simplechrome"""

    test_type: ClassVar[str] = "Simplechrome"
    preinject: ClassVar[bool] = True  # JavaScript injection particular
    waits: ClassVar[Waits] = WAITS
    page: ClassVar[Page] = None
    loop: ClassVar[AbstractEventLoop] = None

    async def goto_test(self) -> Frame:
        """
        Navigate the browser to the test page.

        :return: The frame containing the replayed page
        :rtype: simplechrome.Frame
        """
        try:
            await self.page.goto(self.url, self.waits.net_almost_idle)
        except NavigationTimeoutError:
            pass
        replay_frame = self.page.frames[1]
        return replay_frame
