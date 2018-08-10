import os
from pathlib import Path
from typing import TYPE_CHECKING, Union

import pytest
import uvloop
from jinja2 import Template
from selenium.webdriver import Firefox, Safari, Edge, FirefoxProfile
from selenium.webdriver import Remote
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from simplechrome import Chrome, Page

from test_setup.configurations import configure_test, autowire_test
from test_setup.constants import FIREFOX_EXE, SAUCE_HUB_URL, SAUCE_SAFARI, SAUCE_EDGE
from test_setup.processes import (
    launch_chrome,
    launch_chromium,
    launch_opera,
    launch_wr_player,
    launch_pywb,
)
from test_setup.services import ALL_TESTS
from test_setup.util import has_parent

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.python import Metafunc, FunctionDefinition
    from _pytest.config import Config


__all__ = [
    "pytest_generate_tests",
    "configured",
    "wr_player",
    "pywb",
    "opera",
    "opera_page",
    "chrome",
    "chrome_page",
    "chromium",
    "chromium_page",
    "firefox_driver",
    "edge_driver",
    "safari_driver",
]


def pytest_configure(config: "Config") -> None:
    """Generate the test files before pytest collects"""
    if os.getenv("NOGEN", None) is not None:
        print("no gen")
        return
    test_dir = Path("tests")
    tt_path = Path("test_setup") / "test_template.py.j2"
    manifests_path = Path("manifests")
    with tt_path.open("r") as tin:
        test_template = Template(tin.read(), keep_trailing_newline=True)
    for manifest in manifests_path.glob("*.yml"):
        clean_steam = manifest.stem.strip()
        with (test_dir / f"test_{clean_steam}.py").open("w") as out:
            out.write(
                test_template.render(
                    ALL_TESTS=ALL_TESTS, dsc=clean_steam.upper(), mnfest=str(manifest)
                )
            )


def pytest_generate_tests(metafunc: "Metafunc") -> None:
    """Perform test function setup and parametrization"""
    fndef: "FunctionDefinition" = metafunc.definition
    if fndef.get_marker("autowired"):
        autowire_test(metafunc)


@pytest.fixture(scope="class")
def configured(request: "SubRequest") -> None:
    """Fixture to configure the test class with the manifest information"""
    configure_test(request)
    yield


@pytest.fixture(scope="class")
def wr_player(request: "SubRequest") -> None:
    """Fixture to launch webrecorder player"""
    launch_wr_player(request)
    yield


@pytest.fixture(scope="class")
def pywb(request: "SubRequest") -> None:
    """Fixture to launch pywb"""
    launch_pywb(request)
    yield


@pytest.fixture(scope="class")
def event_loop(request: "SubRequest") -> uvloop.Loop:
    """Fixture for ensure the event loop impl is uvloop"""
    loop = uvloop.new_event_loop()
    if request.cls:
        request.cls.loop = loop
    yield loop
    loop.close()


@pytest.fixture(scope="class")
async def chrome(request: "SubRequest") -> Chrome:
    """Fixture to launch Google Chrome"""
    cls = request.cls
    browser: Chrome = await launch_chrome(cls)
    if not has_parent(request, "new_tab"):
        cls.chrome = browser
    yield browser
    await browser.close()


@pytest.fixture(scope="class")
async def chromium(request: "SubRequest") -> Chrome:
    """Fixture to launch Google Chrome"""
    cls = request.cls
    browser: Chrome = await launch_chromium(cls)
    if not has_parent(request, "new_tab"):
        cls.chrome = browser
    yield browser
    await browser.close()


@pytest.fixture(scope="class")
async def opera(request: "SubRequest") -> Chrome:
    """Fixture to launch Opera"""
    cls = request.cls
    browser: Chrome = await launch_opera(cls)
    if not has_parent(request, "new_tab"):
        cls.chrome = browser
    yield browser
    await browser.close()


@pytest.fixture(scope="class")
async def chrome_page(request: "SubRequest", chrome: Chrome) -> Page:
    """Fixture to launch Google Chrome and receive a new page"""
    cls = request.cls
    page: Page = await chrome.newPage()
    cls.page = page
    if cls.preinject:
        await page.evaluateOnNewDocument(cls.js, raw=True)
    yield page


@pytest.fixture(scope="class")
async def chromium_page(request: "SubRequest", chromium: Chrome) -> Page:
    """Fixture to launch Google Chrome and receive a new page"""
    cls = request.cls
    page: Page = await chromium.newPage()
    cls.page = page
    if cls.preinject:
        await page.evaluateOnNewDocument(cls.js, raw=True)
    yield page


@pytest.fixture(scope="class")
async def opera_page(request: "SubRequest", opera: Chrome) -> Page:
    """Fixture to launch Google Chrome and receive a new page"""
    cls = request.cls
    pages = await opera.pages()
    page: Page = None
    for p in pages:
        if p.url == "about:blank":
            page = p
            break
    cls.page = page
    if cls.preinject:
        await page.evaluateOnNewDocument(cls.js, raw=True)
    yield page


@pytest.fixture(scope="class")
def firefox_driver(request: "SubRequest") -> Firefox:
    """Fixture for receiving selenium controlled FireFox instance"""
    ffp = FirefoxProfile()
    ffp.set_preference("media.volume_scale", "0.0")
    driver = Firefox(
        executable_path=str(request.session.fspath / "bin" / "geckodriver"),
        firefox_binary=FirefoxBinary(FIREFOX_EXE),
        capabilities=dict(marionette=True, acceptInsecureCerts=True),
        firefox_profile=ffp,
    )
    request.cls.driver = driver
    yield driver
    driver.close()


@pytest.fixture(scope="class")
def safari_driver(request: "SubRequest") -> Union[Remote, Safari]:
    """Fixture for receiving selenium controlled Safari instance"""
    if request.cls.test_type == "safari-local":
        driver = Safari()
    else:
        executor = RemoteConnection(SAUCE_HUB_URL, resolve_ip=False)
        driver = Remote(desired_capabilities=SAUCE_SAFARI, command_executor=executor)

    request.cls.driver = driver
    yield driver
    driver.close()


@pytest.fixture(scope="class")
def edge_driver(request: "SubRequest") -> Union[Remote, Edge]:
    """Fixture for receiving selenium controlled Edge instance"""
    if request.cls.test_type == "edge-local":
        driver = Edge()
    else:
        executor = RemoteConnection(SAUCE_HUB_URL, resolve_ip=False)
        driver = Remote(desired_capabilities=SAUCE_EDGE, command_executor=executor)
    request.cls.driver = driver
    yield driver
    driver.close()
