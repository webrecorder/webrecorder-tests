from typing import List, Dict, TYPE_CHECKING, Union
from pathlib import Path

from ruamel.yaml import YAML

if TYPE_CHECKING:
    from py._path.local import LocalPath


__all__ = ["load_file", "load_javascript", "load_manifest", "ConfigT"]

ChromeOptsT = Dict[str, str]
ConfigT = Dict[str, Union[str, List[str], ChromeOptsT]]


def load_file(p: Union["LocalPath", Path, str]) -> str:
    """
    Load a file from disk

    :param p: The path object representing the file
    :return: The contents of the files
    """
    fp = p if not isinstance(p, str) else Path(p)
    with fp.open("r") as iin:
        return iin.read()


def load_manifest(p: Union["LocalPath", Path]) -> ConfigT:
    """
    Loads a tests manifest (yml)

    :param p: The path object representing the manifest
    :return: The contents of the manifest
    """
    with p.open("r") as yamlIn:
        return YAML().load(yamlIn.read())


def load_javascript(
    rootp: Union["LocalPath", Path], load: str
) -> Union[Dict[str, str], List[str], str]:
    """
    Loads the javascript files specified in a test manifest

    :param rootp: The root path to load the javascript from
    :param load: The javascript definition found in a test manifest manifests
    :return: The loaded javascript
    """
    tutil = load_file(Path("testUtils.js"))
    if isinstance(load, dict):
        js_dict: Dict[str, str] = dict()
        for k, v in load.items():
            js_dict[k] = f"{tutil}\n{load_file(rootp / v)}"
        return js_dict
    elif isinstance(load, list):
        js_list: List[str] = list()
        for p in load:
            js_list.append(f"{tutil}\n{load_file(rootp / p)}")
        return js_list
    return f"{tutil}\n{load_file(rootp / load)}"
