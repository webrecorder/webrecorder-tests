import os
import pty
import subprocess
import time
from subprocess import Popen
from typing import Callable, List

import psutil
from _pytest.fixtures import SubRequest
from py._path.local import LocalPath
from simplechrome import launch, Chrome
from urllib.error import URLError
from urllib.request import urlopen

__all__ = ["launch_chrome", "launch_wr_player", "process_reaper", "launch_pywb"]


async def launch_chrome(cls: "WRTest") -> Chrome:
    """
    Launches an instance of the chrome browser.
    If the supplied options exist, the supplied options will be applied before launch.

    :return: Chrome browser object
    """
    opts = getattr(cls, "chrome_opts", None)
    if opts is not None:
        if opts.get("exe"):
            opts["executablePath"] = opts.get("exe")
    else:
        opts = dict()
    if os.getenv("INTRAVIS", None) is not None:
        opts["headless"] = False
    return await launch(options=opts)


def launch_wr_player(request: SubRequest) -> None:
    """Launches an instance of webrecorder player"""
    exe, port, warcp = request.cls.player
    primary, secondary = pty.openpty()
    proc = subprocess.Popen(
        [exe, "--port", port, "--no-browser", warcp], stdout=secondary, stderr=secondary
    )
    request.addfinalizer(process_reaper(proc))
    stdout = os.fdopen(primary)
    while True:
        out = stdout.readline()
        if f"APP_HOST=http://localhost:{port}" in out.rstrip():
            break
    stdout.close()


def warc_glob(p: LocalPath) -> List[str]:
    warcs = []
    for w in p.listdir(fil=lambda x: ".warc" in str(x)):
        warcs.append(str(w))
    return warcs


def launch_pywb(request: SubRequest) -> None:
    """Fixture for launching pywb"""
    rootdir = request.session.fspath
    pywbt = rootdir / "pywb-tests"
    coldir = pywbt / "collections"
    if not coldir.exists():
        warcs = warc_glob(rootdir / "warcs")
        subprocess.run(["wb-manager", "init", "tests"], cwd=str(pywbt))
        subprocess.run(["wb-manager", "add", "tests"] + warcs, cwd=str(pywbt))
    # pywb does not like having its std[out,err] closed suddenly
    proc = subprocess.Popen(
        ["wayback"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(pywbt),
    )
    request.addfinalizer(process_reaper(proc))
    for i in range(100):
        time.sleep(0.1)
        try:
            with urlopen("http://localhost:8080") as f:
                data = f.read().decode()
            break
        except URLError as e:
            continue
    else:
        raise TimeoutError("Could not start server")


def process_reaper(oproc: Popen) -> Callable[[], None]:
    """
    Returns a callable that, once called, will kill the supplied process

    :param oproc: The process to be killed
    :return: A function that will kill the supplied process
    """

    def kill_it() -> None:
        process = psutil.Process(oproc.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

    return kill_it
