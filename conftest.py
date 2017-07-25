import os
import pty
import subprocess
import sys
import time
import signal
import yaml
import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def load_manifest(request):
    """ 
    Load from yaml manifest all metadata of current test 
    class and make them available in self.conf 
    """
    with open('manifest.yml', 'r') as m:
        manifest = yaml.load(m)

    conf = manifest['tests'][request.node.name]

    if request.cls is not None:
        request.cls.conf = conf

    yield conf


@pytest.fixture(scope="class")
def player(request):
    """ 
    starts webrecorder-player with port and warc-file from self.conf
    """
    warc = os.path.join("warcs", request.cls.conf['warc-file'])
    port = request.cls.conf['player_port']

    primary, secondary = pty.openpty()

    player_process = subprocess.Popen(
        ["./bin/webrecorder-player", "--port", port, "--no-browser", warc],
        stdout=secondary, stderr=secondary)

    stdout = os.fdopen(primary)
    while True:
        out = stdout.readline()
        if 'starting server on {port}'.format(port=port) in out.rstrip():
            break

    stdout.close()

    if request.cls is not None:
        request.cls.player = player_process

    yield player_process

    player_process.terminate()
    #subprocess.run(["pkill", "webrecorder-player"])


@pytest.fixture(scope="class")
def browser_driver(request):
    """ 
    starts a selenium driver to a local chrome headless
    the driver is available from self.driver
    TODO: implement logic to use SAUCELABS or remote selenium 
    """
    try:
        chrome = os.environ["CHROME"]
    except KeyError:
        print("set CHROME env to chrome path", file=sys.stderr)
        sys.exit(1)

    opts = webdriver.ChromeOptions()
    opts.binary_location = chrome
    opts.add_argument("headless")
    opts.add_argument("disable-gpu")
    driver = webdriver.Chrome(chrome_options=opts)

    if request.cls is not None:
        request.cls.driver = driver

    yield driver

    driver.close()
    driver.quit()
