from collections import namedtuple
from typing import ClassVar, Optional, Dict

import pytest
from async_timeout import timeout
from grappa import should, expect
from simplechrome import Frame

__all__ = ["WRTest", "WRAutoTest"]

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
        # self.tab.on(self.tab.Events.Console, lambda x: print(x.__dict__))
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
    test_to: ClassVar[int] = 30  # how long to wait for each js function to resolve

    @pytest.mark.asyncio
    async def test_all(self, test_name: str) -> None:
        """Default test method, called once per each test listed in the manifest"""
        replay_frame = await self.goto_test(self.Waits.load)
        async with timeout(self.test_to) as to:
            results = await replay_frame.evaluate(f"{test_name}()")
        if to.expired:
            raise WRAutoTestTimeOut(f"{test_name} did not resolve within 30 seconds")
        results | self.should.be.true
