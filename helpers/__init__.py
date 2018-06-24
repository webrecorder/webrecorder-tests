from pathlib import Path
import os
from typing import ClassVar

import uvloop
import yaml
from grappa import should, expect
from grappa.test_proxy import TestProxy
from simplechrome import Page


def load_conifg(root: str, path: str) -> dict:
    confp = Path(root, path)
    with confp.open("r") as iin:
        return yaml.load(iin)


class Context(object):
    should: ClassVar[should] = should
    expect: ClassVar[expect] = expect

    def __init__(self, loop: uvloop.Loop, page: Page, url: str):
        self.loop: uvloop.Loop = loop
        self.page: Page = page
        self.url: str = url
