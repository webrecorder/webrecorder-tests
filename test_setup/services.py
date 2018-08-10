from typing import List, Tuple

import pytest

from .browsers import (
    ChromeTest,
    ChromiumTest,
    OperaTest,
    FireFoxTest,
    SafariTest,
    EdgeTest,
)

try:
    import pywb

    HAVE_PYWB = True
except ImportError:
    HAVE_PYWB = False

__all__ = [
    "PywbOperaTest",
    "PywbChromiumTest",
    "PywbChromeTest",
    "PywbFireFoxTest",
    "PywbEdgeTest",
    "PywbSafariTest",
    "WRPlayerOperaTest",
    "WRPlayerChromeTest",
    "WRPlayerChromiumTest",
    "WRPlayerFireFoxTest",
    "WRPlayerSafariTest",
    "WRPlayerEdgeTest",
    "ALL_TESTS",
]

PYWB_SKIP_REASON = "Pywb is not installed. To test using pywb, please execute 'pip install -r test-requirements.txt'"


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbChromeTest(ChromeTest):
    """Class automatically requiring fixtures for pywb testing using the Chrome browser"""


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbChromiumTest(ChromiumTest):
    """Class automatically requiring fixtures for pywb testing using the Chromium browser"""


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbOperaTest(OperaTest):
    """Class automatically requiring fixtures for pywb testing using the Opera browser"""


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbFireFoxTest(FireFoxTest):
    """Class automatically requiring fixtures for pywb testing using the FireFox browser"""


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbSafariTest(SafariTest):
    """Class automatically requiring fixtures for pywb testing using the Safari browser"""


@pytest.mark.skipif(not HAVE_PYWB, reason=PYWB_SKIP_REASON)
@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb")
class PywbEdgeTest(EdgeTest):
    """Class automatically requiring fixtures for pywb testing using the Edge browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerChromeTest(ChromeTest):
    """Class automatically requiring fixtures for wr player testing using the Chrome browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerChromiumTest(ChromiumTest):
    """Class automatically requiring fixtures for wr player testing using the Chromium browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerOperaTest(OperaTest):
    """Class automatically requiring fixtures for wr player testing using the Opera browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerFireFoxTest(FireFoxTest):
    """Class automatically requiring fixtures for wr player testing using the FireFox browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerSafariTest(SafariTest):
    """Class automatically requiring fixtures for wr player testing using the Safari browser"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player")
class WRPlayerEdgeTest(EdgeTest):
    """Class automatically requiring fixtures for wr player testing using the Edge browser"""


ALL_TESTS: List[Tuple[str, str]] = [
    # Test Kind    Test Class
    ("PywbOpera", "PywbOperaTest"),
    ("PywbChrome", "PywbChromeTest"),
    ("PywbChromium", "PywbChromiumTest"),
    ("PywbFireFox", "PywbFireFoxTest"),
    ("PywbSafari", "PywbSafariTest"),
    ("PywbEdge", "PywbEdgeTest"),
    ("WRPlayerOpera", "WRPlayerOperaTest"),
    ("WRPlayerChrome", "WRPlayerChromeTest"),
    ("WRPlayerChromium", "WRPlayerChromiumTest"),
    ("WRPlayerFireFox", "WRPlayerFireFoxTest"),
    ("WRPlayerSafari", "WRPlayerSafariTest"),
    ("WRPlayerEdge", "WRPlayerEdgeTest"),
]
