from .wrtest import PywbTest, WRPlayerTest


class TestWikipediaSopa(WRPlayerTest):
    manifest = "manifests/wikisopa.yml"


class TestWikipediaSopaPywb(PywbTest):
    manifest = "manifests/wikisopa.yml"
