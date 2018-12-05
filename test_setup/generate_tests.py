"""Module containing test setup methods"""
import string
from pathlib import Path

from jinja2 import Template

from .loaders import load_manifest

__all__ = ["gen"]


def load_test_setup_str(test_setup_dir) -> str:
    return f'load_file("{test_setup_dir / "testUtil.js"}")'


def load_test_js_str(root_dir: Path, js_path: str) -> str:
    return f'load_file("{root_dir / js_path}")'


def load_template(template_dir: Path) -> Template:
    header = template_dir / "testHeader.py.j2"
    chrome = template_dir / "chromeBasedTests.py.j2"
    selenium = template_dir / "seleniumBasedTests.py.j2"
    with header.open("r") as htin, chrome.open("r") as ctin, selenium.open("r") as stin:
        return Template(
            htin.read() + ctin.read() + stin.read(), keep_trailing_newline=True
        )


def gen(root_dir: Path) -> None:
    """Auto-generates the tests.

    :param root_dir: The absolute path to the webrecorder-tests directory
    """
    test_dir: Path = root_dir / "tests"
    test_setup_dir: Path = root_dir / "test_setup"
    test_template = load_template(test_setup_dir / "templates")
    clean_test_name = str.maketrans({key: None for key in string.punctuation})
    for manifestPath in (root_dir / "manifests").glob("*.yml"):
        test_name = manifestPath.stem.strip().translate(clean_test_name)
        with (test_dir / f"test_{test_name}.py").open("w") as out:
            manifest = load_manifest(manifestPath)
            has_js = "javascript" in manifest
            test_conf = dict(
                chrome_opts=manifest.get("chrome"),
                test_list=str(manifest.get("tests")),
                player_info=(
                    str(root_dir / "bin/webrecorder-player"),
                    "8092",
                    str(root_dir / manifest.get("warc-file")),
                ),
                player_url=f"http://localhost:8092/local/collection/{manifest.get('time')}/{manifest.get('url')}",
                pywb_url=f"http://localhost:8080/tests/{manifest.get('time')}/{manifest.get('url')}",
                has_js=has_js,
                manifestPath=manifestPath,
            )
            test_conf["test_util"] = load_test_setup_str(test_setup_dir)
            if has_js:
                test_conf["js"] = load_test_js_str(root_dir, manifest.get("javascript"))
            out.write(test_template.render(test_conf))
