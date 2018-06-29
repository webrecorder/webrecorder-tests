from pathlib import Path
from typing import Union, Dict, List

import yaml
from py._path.local import LocalPath

__all__ = ["load_file", "load_javascript", "load_manifest"]

LoadJS = Union[Dict[str, str], List[str], str]


def load_file(p: Union[LocalPath, Path]) -> str:
    """
    Load a file from disk

    :param p: The path object representing the file
    :return: The contents of the files
    """
    with p.open("r") as iin:
        return iin.read()


def load_manifest(p: Union[LocalPath, Path]) -> dict:
    """
    Loads a tests manifest (yml)

    :param p: The path object representing the manifest
    :return: The contents of the manifest
    """
    return yaml.load(load_file(p))


def load_javascript(rootp: Union[LocalPath, Path], load: LoadJS) -> LoadJS:
    """
    Loads the javascript files specified in a test manifest

    :param rootp: The root path to load the javascript from
    :param load: The javascript definition found in a test manifest manifests
    :return: The loaded javascript
    """
    if isinstance(load, dict):
        js = dict()
        for k, v in load.items():
            js[k] = load_file(rootp / v)
    elif isinstance(load, list):
        js = list()
        for p in load:
            js.append(load_file(rootp / p))
    else:
        js = load_file(rootp / load)
    return js
