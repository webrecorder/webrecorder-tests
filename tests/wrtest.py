from collections import namedtuple
from typing import ClassVar, Optional, Dict, Union

import pytest
from async_timeout import timeout
from grappa import should, expect
from simplechrome import Frame

__all__ = ["WRTest", "WRAutoTest", "PywbTest", "WRPlayerTest"]

WAITS = namedtuple("WAITS", ["load", "dom_load", "net_idle", "net_almost_idle"])


class WRAutoTestTimeOut(Exception):
    """Class to indicate an auto-test did not run complete within a time limit"""


class WRTest(object):
    """Base Webrecorder Test class. Home to utilities used by all tests"""

    manifest: ClassVar[str] = None  # Path to manifest to be used by the test
    preinject: ClassVar[bool] = False  # JavaScript injection particular
    should: ClassVar[should] = should  # Should style assertions
    expect: ClassVar[expect] = expect  # Expect style assertions
    Waits: ClassVar[WAITS] = WAITS(
        load=dict(waitUntil="load"),
        dom_load=dict(waitUntil="documentloaded"),
        net_idle=dict(waitUntil="networkidle0"),
        net_almost_idle=dict(waitUntil="networkidle2"),
    )

    async def goto_test(self, wait: Optional[Dict[str, str]] = None) -> Frame:
        """
        Navigate the browser to the test page.
        Optionally waiting for a specific browser event.

        :param wait: Optional wait for event to happen
        :type wait: WAITS
        :return: The frame containing the replayed page
        :rtype: simplechrome.Frame
        """
        await self.page.goto(self.url, self.Waits.dom_load)
        replay_frame = self.page.frames[1]
        replay_frame.enable_lifecycle_emitting()
        await replay_frame.navigation_waiter(loop=self.loop, timeout=5)
        if wait is not None:
            if wait == self.Waits.load:
                await replay_frame.loaded_waiter(loop=self.loop, timeout=15)
            elif wait == self.Waits.net_idle:
                await replay_frame.network_idle_waiter(loop=self.loop, timeout=15)
        return replay_frame


@pytest.mark.autowired
class WRAutoTest(WRTest):
    """Base class for tests that supply only a manifest"""

    preinject = True
    test_to: ClassVar[Union[int, float]] = 30  # how long to wait for each js function to resolve

    @pytest.mark.asyncio
    async def test_all(self, test_name: str) -> None:
        """Default test method, called once per each test listed in the manifest"""
        replay_frame = await self.goto_test(self.Waits.load)
        async with timeout(self.test_to) as to:
            results = await replay_frame.evaluate(f"{test_name}()")
        if to.expired:
            raise WRAutoTestTimeOut(
                f"{test_name} did not resolve within {self.test_to} seconds"
            )
        results | self.should.be.true


@pytest.mark.pywbtest
@pytest.mark.usefixtures("pywb", "chrome_page")
class PywbTest(WRAutoTest):
    """Class automatically requiring fixtures for pywb testing"""


@pytest.mark.wrplayertest
@pytest.mark.usefixtures("wr_player", "chrome_page")
class WRPlayerTest(WRAutoTest):
    """Class automatically requiring fixtures for wr player testing"""
