import pytest
from .wrtest import WRAutoTest


@pytest.mark.usefixtures("wr_player", "chrome_page")
class TestYouTube(WRAutoTest):
    manifest = "manifests/youtube.yml"
