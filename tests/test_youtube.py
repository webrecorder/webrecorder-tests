from .wrtest import WRPlayerTest, PywbTest


class TestYouTubePlayer(WRPlayerTest):
    manifest = "manifests/youtube.yml"


class TestYouTubePYWB(PywbTest):
    manifest = "manifests/youtube.yml"
