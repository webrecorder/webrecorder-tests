import os
from shutil import which
from typing import Dict, Optional, List, Union

import attr

__all__ = [
    "Waits",
    "WAITS",
    "CHROME_EXE",
    "FIREFOX_EXE",
    "SAFARI_EXE",
    "OPERA_EXE",
    "EDGE_EXE",
    "TRAVIS_TUNNEL_ID",
    "SAUCE_HUB_URL",
    "SAUCE_EDGE",
    "SAUCE_SAFARI",
]


def find_chrome() -> Optional[str]:
    """Finds an the path the a locally installed Chrome browser"""
    for browser in (
        "google-chrome-unstable",
        "google-chrome-beta",
        "google-chrome",
        "chrome",
        "browsers",
        "browsers-browser",
    ):
        if which(browser):
            return browser
    return None


def find_firefox() -> Optional[str]:
    """Finds an the path the a locally installed FireFox browser"""
    for browser in (
        "firefox",
        "mozilla-firefox",
        "mozilla-firebird",
        "firebird",
        "mozilla",
        "netscape",
    ):
        if which(browser):
            return browser
    return None


@attr.dataclass(slots=True)
class Waits(object):
    """Immutable class holding the waits used in simple chrome"""

    load: Dict[str, str] = attr.ib(default=dict(waitUntil="load"))
    dom_load: Dict[str, str] = attr.ib(default=dict(waitUntil="documentloaded"))
    net_idle: Dict[str, str] = attr.ib(default=dict(waitUntil="networkidle0"))
    net_almost_idle: Dict[str, str] = attr.ib(default=dict(waitUntil="networkidle1"))


WAITS = Waits()
CHROME_EXE: Optional[str] = find_chrome()
FIREFOX_EXE: Optional[str] = find_firefox()
OPERA_EXE: Optional[str] = which("opera")
SAFARI_EXE: Optional[str] = which("safari")
EDGE_EXE: Optional[str] = which("edge")

TRAVIS_TUNNEL_ID: Optional[str] = os.getenv("TRAVIS_JOB_NUMBER")
TRAVIS_BUILD: Optional[str] = os.getenv("TRAVIS_BUILD_NUMBER")
SAUCE_TAGS: List[Union[Optional[str], str]] = [os.getenv("TRAVIS_PYTHON_VERSION"), "CI"]

SAUCE_USERNAME: Optional[str] = os.getenv(
    "SAUCE_USERNAME", os.getenv("SAUCE_USERNAME2", None)
)
SAUCE_KEY: Optional[str] = os.getenv("SAUCE_ACCESS_KEY")


SAUCE_HUB_URL = f"http://{SAUCE_USERNAME}:{SAUCE_KEY}@ondemand.saucelabs.com:80/wd/hub"


SAUCE_EDGE = {
    "browserName": "MicrosoftEdge",
    "platform": "Windows 10",
    "version": "17.17134",
    "tunnelIdentifier": TRAVIS_TUNNEL_ID,
    "build": TRAVIS_BUILD,
    "tags": [os.getenv("TRAVIS_PYTHON_VERSION"), "CI", "EDGE"],
}

SAUCE_IE = {
    "browserName": "internet explorer",
    "platform": "Windows 10",
    "version": "11.103",
    "tunnelIdentifier": TRAVIS_TUNNEL_ID,
    "build": TRAVIS_BUILD,
    "tags": [os.getenv("TRAVIS_PYTHON_VERSION"), "CI", "IE"],
}

SAUCE_SAFARI = {
    "browserName": "safari",
    "platform": "macOS 10.13",
    "version": "11.1",
    "tunnelIdentifier": TRAVIS_TUNNEL_ID,
    "build": TRAVIS_BUILD,
    "tags": [os.getenv("TRAVIS_PYTHON_VERSION"), "CI", "SAFARI"],
}
