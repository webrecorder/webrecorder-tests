import pytest
from async_timeout import timeout
from .wrtest import WRTest


@pytest.mark.usefixtures("configured", "player", "new_tab")
class TestWikipediaSopa(WRTest):
    manifest = "manifests/wikisopa.yml"

    @pytest.mark.asyncio
    async def test_sopa_overlay(self):
        replay_frame = await self.goto_test()
        async with timeout(10) as to:
            await replay_frame.waitFor("#mw-sopaOverlay")
        overlay = await replay_frame.J("#mw-sopaOverlay")
        text = await replay_frame.evaluate(self.js.get("overlay"), overlay)
        text | self.should.be.equal.to("Imagine a World")
