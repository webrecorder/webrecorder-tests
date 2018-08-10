from typing import ClassVar

import pytest

from test_setup.constants import (
    CHROME_EXE,
    OPERA_EXE,
    EDGE_EXE,
    FIREFOX_EXE,
    SAFARI_EXE,
    TRAVIS_TUNNEL_ID,
)
from .wrtest import WRSimpleChromeTest, WRSeleniumTest

__all__ = [
    "ChromiumTest",
    "ChromeTest",
    "OperaTest",
    "FireFoxTest",
    "SafariTest",
    "EdgeTest",
]


@pytest.mark.chromiumtest
@pytest.mark.usefixtures("chromium_page")
class ChromiumTest(WRSimpleChromeTest):
    """Base class for using the Chromium browser"""

    test_type: ClassVar[str] = "browsers"


@pytest.mark.skipif(CHROME_EXE is None, reason="Chrome Is Not Installed")
@pytest.mark.chrometest
@pytest.mark.usefixtures("chrome_page")
class ChromeTest(WRSimpleChromeTest):
    """Base class for using the Chrome browser"""

    test_type: ClassVar[str] = "chrome"


@pytest.mark.skipif(OPERA_EXE is None, reason="Opera Is Not Installed")
@pytest.mark.operatest
@pytest.mark.usefixtures("opera_page")
class OperaTest(WRSimpleChromeTest):
    """Base class for using the Opera browser"""

    test_type: ClassVar[str] = "opera"


@pytest.mark.skipif(FIREFOX_EXE is None, reason="FireFox Is Not Installed")
@pytest.mark.firefoxtest
@pytest.mark.usefixtures("firefox_driver")
class FireFoxTest(WRSeleniumTest):
    """Base class for using the FireFox browser"""

    test_type: ClassVar[str] = "firefox"


@pytest.mark.skipif(
    TRAVIS_TUNNEL_ID is None and SAFARI_EXE is None,
    reason="Safari Testing On Non-OSX Machines Requires Travis",
)
@pytest.mark.safaritest
@pytest.mark.usefixtures("safari_driver")
class SafariTest(WRSeleniumTest):
    """Base class for using the Safari browser (locally or via saucelabs)"""

    test_type: ClassVar[
        str
    ] = "safari-sauce" if TRAVIS_TUNNEL_ID is not None else "safari-local"


@pytest.mark.skipif(
    TRAVIS_TUNNEL_ID is None and EDGE_EXE is None,
    reason="Edge Testing On Non-Windows Machines Requires Travis",
)
@pytest.mark.safaritest
@pytest.mark.usefixtures("edge_driver")
class EdgeTest(WRSeleniumTest):
    """Base class for using the Safari browser (locally or via saucelabs)"""

    test_type: ClassVar[
        str
    ] = "edge-sauce" if TRAVIS_TUNNEL_ID is not None else "edge-local"
