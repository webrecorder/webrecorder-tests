import pytest
from helpers import Context


@pytest.mark.usemanifest("manifest2.yml")
@pytest.mark.asyncio
async def test_it(ctx: Context):
    await ctx.page.goto(ctx.url, dict(waitUntil="documentloaded"))
    replay_frame = ctx.page.frames[1]
    replay_frame.enable_lifecycle_emitting()
    await replay_frame.navigation_waiter(loop=ctx.loop, timeout=5)
    await replay_frame.network_idle_waiter(loop=ctx.loop, timeout=15)
    await replay_frame.title() | ctx.should.be.equal.to(
        "Procrastination Polka by Dragan Espenschied (Live) - YouTube"
    )
