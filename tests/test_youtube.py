import pytest
from .wrtest import WRTest


@pytest.mark.usefixtures("configured", "player", "new_tab")
class TestYouTube(WRTest):
    manifest = "manifests/youtube.yml"

    @pytest.mark.asyncio
    async def test_title(self):
        replay_frame = await self.goto_test(wait=self.Waits.net_idle)
        await replay_frame.title() | self.should.be.equal.to(
            "Procrastination Polka by Dragan Espenschied (Live) - YouTube"
        )

    @pytest.mark.asyncio
    async def test_video_src(self):
        replay_frame = await self.goto_test(wait=self.Waits.net_idle)
        video_src = await replay_frame.evaluate(self.js.get("video_src"))
        video_src | self.should.be.equal.to(
            "https://r2---sn-nvopjoxu-25ve.googlevideo.com/videoplayback?lmt=1293668212190294&expire=1490092899&ratebypass=yes&ipbits=0&mime=video%2Fmp4&requiressl=yes&clen=8924242&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpcm2cms%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=2363750&pl=19&source=youtube&dur=116.471&mv=m&mt=1490071223&ms=au&ei=A6_QWLyRKe-A_APRtI7wDQ&id=o-ABvUC5LhDBxHMoY_fDgjpktcyl8manKZR09X3CE-g53X&mn=sn-nvopjoxu-25ve&mm=31&signature=D59DC089448E0C9FBBA80512A5C2D87A01AC75D1.65AF95645D26D34CDE542DFC13F0464F156F03C3&key=yt6&ip=75.101.62.254&gir=yes&upn=9P176uePWno&pcm2cms=yes&itag=18&cpn=JOlTjRyzZpdp9YNl&c=WEB&cver=1.20170316&ptk=youtube_none&pltype=contentugc"
        )

    @pytest.mark.asyncio
    async def test_video_duration(self):
        replay_frame = await self.goto_test(wait=self.Waits.net_idle)
        duration = await replay_frame.evaluate(self.js.get("video_duration"))
        duration | self.should.be.equal.to(116.471293)

    @pytest.mark.skip(reason="chrome does not autoplay video anymore")
    @pytest.mark.asyncio
    async def test_video_playing(self):
        replay_frame = await self.goto_test(wait=self.Waits.net_idle)
        playing = await replay_frame.evaluate(self.js.get("video_playing"))
        playing | self.should.be.equal.to("play")
