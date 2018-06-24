import asyncio
import os
from typing import Generator, AsyncGenerator, Any

import pytest
import uvloop
from _pytest.fixtures import SubRequest
from _pytest.mark import MarkInfo
from _pytest.python import FunctionDefinition
from _pytest.python import Metafunc
from aiohttp import ClientSession, ClientConnectorError
from async_timeout import timeout
from simplechrome import Chrome
from simplechrome import launch

from helpers import load_conifg, Context


def pytest_generate_tests(metafunc: Metafunc):
    fndef: FunctionDefinition = metafunc.definition
    uconfm: MarkInfo = fndef.get_marker("usemanifest")
    if uconfm:
        rootdir = metafunc.config.rootdir
        config = load_conifg(rootdir, uconfm.args[0])
        warcp = os.path.join(rootdir, "warcs", config["warc-file"])
        cntx_seed = dict(
            player=dict(
                exe=os.path.join(rootdir, "bin/webrecorder-player"),
                port=f"{config.get('player_port')}",
                warcp=warcp,
            ),
            url=(
                f"http://localhost:{config.get('player_port')}/local/collection/"
                f"{config.get('time')}/{config.get('url')}"
            ),
        )
        # local/collection/{time}/{url}
        metafunc.parametrize("ctx", [cntx_seed], True)
        # print(Path(confp, os.getcwd()), '\n')
        # print(Path(os.getcwd(), confp), '\n')
        # print(confp, os.getcwd(), '\n')


@pytest.yield_fixture()
def event_loop() -> Generator[uvloop.Loop, Any, None]:
    loop = uvloop.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def chrome() -> AsyncGenerator[Chrome, Any]:
    chrome = await launch()
    yield chrome
    try:
        await chrome.close()
    except:
        pass


async def check_player(url: str) -> None:
    async with ClientSession() as session:
        for _ in range(100):
            await asyncio.sleep(0.5)
            try:
                await session.get(url)
                break
            except ClientConnectorError as cce:
                print(cce)
                continue


async def create_player(exe: str, port: str, warcp: str, loop: uvloop.Loop):
    process = await asyncio.create_subprocess_exec(
        *[exe, "--port", port, "--no-browser", warcp],
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
        loop=loop,
    )
    async with timeout(10) as to:
        await check_player(f"http://localhost:{port}")
    return process


@pytest.fixture
async def ctx(
    request: SubRequest, event_loop: uvloop.Loop, chrome: Chrome
) -> AsyncGenerator[Context, Any]:
    seed = request.param
    player = seed.get("player")
    print(player, "\n")
    pprocess = await create_player(
        player.get("exe"), player.get("port"), player.get("warcp"), event_loop
    )
    page = await chrome.newPage()
    request.addfinalizer(lambda: pprocess.terminate())
    yield Context(event_loop, page, seed.get("url"))
    # async with aiofiles.open(request.param) as iin:
    #     mnfst = yaml.load(await iin.read())
    # return mnfst
