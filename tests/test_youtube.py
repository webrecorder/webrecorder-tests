import pytest


@pytest.mark.usefixtures("load_manifest", "player", "browser_driver")
class TestYoutube(object):

    def test_manifest_loading(self):
        assert self.conf['warc-file'] == "yt-20170330012230.warc.gz"

    def test_recordings_number(self):
        assert len(self.conf['recordings']) == 2

    def test_title(self):
        url = self.conf['recordings'][0]['url']
        time = self.conf['recordings'][0]['time']
        port = self.conf['player_port']
        player_url = f'http://localhost:{port}/local/collection/{time}/{url}'

        self.driver.get(player_url)

        assert self.driver.title == "Procrastination Polka by Dragan Espenschied (Live) - YouTube (Archived)"
