import os
import pty
import subprocess
from subprocess import Popen
from typing import Callable

import psutil
from _pytest.fixtures import SubRequest
from simplechrome import launch, Chrome

__all__ = ["launch_chrome", "launch_wr_player", "process_reaper"]


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


