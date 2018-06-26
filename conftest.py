import collections
import os
import pty
import subprocess
from typing import Generator, AsyncGenerator, Any, Optional

import psutil
import pytest
import uvloop
import yaml
from _pytest.fixtures import SubRequest
from simplechrome import Chrome, Page
from simplechrome import launch


def reaper(oproc):
    def kill_it():
        process = psutil.Process(oproc.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

    return kill_it


def load_file(p) -> str:
    with p.open("r") as iin:
        return iin.read()


def has_parent(request: SubRequest, parent_name: str) -> bool:
    parent = getattr(request, "_parent_request", None)
    if parent is not None:
        return parent.fixturename == parent_name
    return False


async def safe_launch(opts: Optional[dict]) -> Chrome:
    if opts is not None:
        if opts.get("exe"):
            opts["executablePath"] = opts.get("exe")
    return await launch(options=opts)


@pytest.fixture(scope="class")
def configured(request: SubRequest) -> None:
    cls = request.cls
    mani_p = cls.manifest
    fspath = request.session.fspath
    config = yaml.load(load_file(fspath / mani_p))
    cls.player = (
        str(fspath / "bin/webrecorder-player"),
        f"{config.get('player_port')}",
        config["warc-file"],
    )
    _js = config.get("javascript")
    if _js:
        if isinstance(_js, dict):
            js = dict()
            for k, v in _js.items():
                js[k] = load_file(fspath / v)
        elif isinstance(_js, collections.Iterable):
            js = list()
            for p in _js:
                js.append(load_file(fspath / p))
        else:
            js = load_file(fspath / _js)
        cls.js = js
    cls.url = (
        f"http://localhost:{config.get('player_port')}/local/collection/"
        f"{config.get('time')}/{config.get('url')}"
    )
    cls.chrome_opts = config.get("chrome")
    yield


@pytest.fixture(scope="class")
def player(request: SubRequest) -> None:
    exe, port, warcp = request.cls.player
    primary, secondary = pty.openpty()
    proc = subprocess.Popen(
        [exe, "--port", port, "--no-browser", warcp], stdout=secondary, stderr=secondary
    )
    request.addfinalizer(reaper(proc))
    stdout = os.fdopen(primary)
    while True:
        out = stdout.readline()
        if f"APP_HOST=http://localhost:{port}" in out.rstrip():
            break
    stdout.close()
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
    cls = request.cls
    browser = await safe_launch(getattr(cls, "chrome_opts", None))
    if not has_parent(request, "new_tab"):
        cls.chrome = browser
    yield browser
    await browser.close()


@pytest.fixture(scope="class")
async def new_tab(request: SubRequest, chrome: Chrome) -> AsyncGenerator[Page, Any]:
    page = await chrome.newPage()
    request.cls.tab = page
    yield page
