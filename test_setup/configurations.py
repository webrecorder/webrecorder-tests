"""Module containing test setup methods"""

from pathlib import Path
from typing import Union

from _pytest.fixtures import SubRequest
from _pytest.python import Metafunc
from py._path.local import LocalPath

from .loaders import load_manifest, load_javascript

__all__ = ["autowire_test", "configure_test"]


def _default_test_setup(root: Union[LocalPath, Path], config: dict, cls: "WRTest") -> None:
    cls.player = (
        str(root / "bin/webrecorder-player"),
        f"{config.get('player_port')}",
        config.get("warc-file"),
    )
    _js = config.get("javascript")
    if _js:
        cls.js = load_javascript(root, _js)
    cls.url = (
        f"http://localhost:{config.get('player_port')}/local/collection/"
        f"{config.get('time')}/{config.get('url')}"
    )
    cls.chrome_opts = config.get("chrome")


def autowire_test(metafunc: Metafunc) -> None:
    """Autowire a WRAutoTest."""
    cls = metafunc.cls
    rootdir = metafunc.config.rootdir
    config = load_manifest(rootdir / cls.manifest)
    _default_test_setup(rootdir, config, cls)
    cls.autoinject = True
    metafunc.parametrize('test_name', config.get('tests'))


def configure_test(request: SubRequest) -> None:
    """Configure a test using the manifest class property"""
    mani_p = request.cls.manifest
    rootdir = request.session.fspath
    config = load_manifest(rootdir / mani_p)
    _default_test_setup(rootdir, config, request.cls)
