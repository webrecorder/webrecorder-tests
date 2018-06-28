from typing import Generator, AsyncGenerator, Any

import pytest
import uvloop
from _pytest.fixtures import SubRequest
from _pytest.python import Metafunc, FunctionDefinition
from simplechrome import Chrome, Page

from test_setup.configurations import autowire_test, configure_test
from test_setup.processes import launch_chrome, launch_wr_player
from test_setup.util import has_parent


def pytest_generate_tests(metafunc: Metafunc):
    fndef: FunctionDefinition = metafunc.definition
    if fndef.get_marker("autowired"):
        autowire_test(metafunc)


@pytest.fixture(scope="class")
def configured(request: SubRequest) -> None:
    """Fixture to configure the test class with the manifest information"""
    configure_test(request)
    yield


@pytest.fixture(scope="class")
def wr_player(request: SubRequest) -> None:
    """Fixture to launch webrecorder player"""
    launch_wr_player(request)
    yield


@pytest.fixture(scope="class")
def event_loop(request: SubRequest) -> Generator[uvloop.Loop, Any, None]:
    loop = uvloop.new_event_loop()
    if request.cls:
        request.cls.loop = loop
    yield loop
    loop.close()


@pytest.fixture(scope="class")
async def chrome(request: SubRequest) -> AsyncGenerator[Chrome, Any]:
    """Fixture to launch Google Chrome"""
    cls = request.cls
    browser = await launch_chrome(cls)
    if not has_parent(request, "new_tab"):
        cls.chrome = browser
    yield browser
    await browser.close()


@pytest.fixture(scope="class")
async def chrome_page(request: SubRequest, chrome: Chrome) -> AsyncGenerator[Page, Any]:
    """Fixture to launch Google Chrome and receive a new page"""
    cls = request.cls
    page = await chrome.newPage()
    cls.page = page
    if cls.preinject:
        await page.evaluateOnNewDocument(cls.js, raw=True)
    yield page

