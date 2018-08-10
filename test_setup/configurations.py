"""Module containing test setup methods"""

from typing import List, TYPE_CHECKING, Dict

from .loaders import load_manifest, load_file

if TYPE_CHECKING:
    from py._path.local import LocalPath
    from _pytest.fixtures import SubRequest
    from _pytest.python import Metafunc
    from .wrtest import WRTest

__all__ = ["autowire_test", "configure_test"]


def setup_url(fixturenames: List[str], config: Dict) -> str:
    """Constructs the correct url for the test based on the fixture name"""
    if "wr_player" in fixturenames:
        return (
            f"http://localhost:8092/local/collection/"
            f"{config.get('time')}/{config.get('url')}"
        )
    return f"http://localhost:8080/tests/{config.get('time')}/{config.get('url')}"


def _default_test_setup(
    root: "LocalPath", fixturenames: List[str], config: Dict, cls: "WRTest"
) -> None:
    cls.player = (str(root / "bin/webrecorder-player"), "8092", config.get("warc-file"))
    _js = config.get("javascript")
    if _js:
        cls.js = load_file(root / _js)
    cls.url = setup_url(fixturenames, config)
    cls.chrome_opts = config.get("chrome")


def autowire_test(metafunc: "Metafunc") -> None:
    """Autowire a WRAutoTest."""
    cls = metafunc.cls
    rootdir = metafunc.config.rootdir
    config = load_manifest(rootdir / cls.manifest)
    _default_test_setup(rootdir, metafunc.fixturenames, config, cls)
    metafunc.parametrize("test_name", config.get("tests"))


def configure_test(request: "SubRequest") -> None:
    """Configure a test using the manifest class property"""
    mani_p = request.cls.manifest
    rootdir = request.session.fspath
    config = load_manifest(rootdir / mani_p)
    _default_test_setup(rootdir, request.fixturenames, config, request.cls)
