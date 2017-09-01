import pytest


@pytest.mark.usefixtures("load_manifest", "player", "browser_driver")
class TestYoutube(object):

    def test_title(self):
        url = self.conf['recordings'][0]['url']
        time = self.conf['recordings'][0]['time']
        port = self.conf['player_port']
        player_url = 'http://localhost:{port}/local/collection/{time}/{url}'.format(
            port=port, time=time, url=url)

        self.driver.get(player_url)

        assert self.driver.title == "Procrastination Polka by Dragan Espenschied (Live) - YouTube (Archived)"

    def test_video_src(self):
        url = self.conf['recordings'][0]['url']
        time = self.conf['recordings'][0]['time']
        port = self.conf['player_port']
        player_url = 'http://localhost:{port}/local/collection/{time}/{url}'.format(
            port=port, time=time, url=url)

        self.driver.get(player_url)
        js = open("js/youtube/video_src.js", 'r').read()

        video_src = self.driver.execute_script(js)
        assert video_src == "https://r3---sn-p5qlsnle.googlevideo.com/videoplayback?dur=116.471&mime=video%2Fmp4&itag=18&upn=pliHG8v29a0&source=youtube&mm=31&ip=54.84.117.210&ratebypass=yes&requiressl=yes&mv=m&id=o-AAMsgg3G5ytCoPqdjuiBBt9w83snws-HUxSAGuejWt0s&ms=au&key=yt5&initcwndbps=25113750&mt=1420874344&expire=1420896014&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cnh%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&nh=IgpwcjAxLmlhZDI2KgkxMjcuMC4wLjE&ipbits=0&signature=0BCCCE8465169245EECA421109BFFD0C55ABD435.114D7116D94EA48F906416DA2EA71C5D2E1EC4C0&sver=3&fexp=900718%2C917000%2C919145%2C927622%2C932404%2C938682%2C9405768%2C941004%2C943917%2C947209%2C947218%2C947225%2C948124%2C948527%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&cpn=Cs87iY7UpiTakYUU&ptk=youtube_none&pltype=contentugc&c=WEB&cver=html5"
