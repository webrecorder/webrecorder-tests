from typing import ClassVar, Optional

from collections import namedtuple
from simplechrome import Frame
from grappa import should, expect

__all__ = ["WRTest"]

WAITS = namedtuple("WAITS", ["load", "dom_load", "net_idle", "net_almost_idle"])


class WRTest(object):
    """Base Webrecorder Test class. Home to utilities used by all tests"""

    should: ClassVar[should] = should
    expect: ClassVar[expect] = expect
    Waits: ClassVar[WAITS] = WAITS(
        load=dict(waitUntil="load"),
        dom_load=dict(waitUntil="documentloaded"),
        net_idle=dict(waitUntil="networkidle0"),
        net_almost_idle=dict(waitUntil="networkidle2"),
    )

    async def goto_test(self, wait: Optional[WAITS] = None) -> Frame:
        """
        Navigate the browser to the test page.
        Optionally waiting for a specific browser event.

        :param wait: Optional wait for event to happen
        :type wait: WAITS
        :return: The frame containing the replayed page
        :rtype: simplechrome.Frame
        """
        await self.tab.goto(self.url, self.Waits.dom_load)
        replay_frame = self.tab.frames[1]
        replay_frame.enable_lifecycle_emitting()
        await replay_frame.navigation_waiter(loop=self.loop, timeout=5)
        if wait is not None:
            if wait == self.Waits.load:
                await replay_frame.loaded_waiter(loop=self.loop, timeout=15)
            elif wait == self.Waits.net_idle:
                await replay_frame.network_idle_waiter(loop=self.loop, timeout=15)
        return replay_frame
