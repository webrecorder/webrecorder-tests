import pytest
from .wrtest import WRAutoTest


@pytest.mark.usefixtures("wr_player", "chrome_page")
class TestWikipediaSopa(WRAutoTest):
    manifest = "manifests/wikisopa.yml"
