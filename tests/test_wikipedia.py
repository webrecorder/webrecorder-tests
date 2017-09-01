import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("load_manifest", "player", "browser_driver")
class TestWikipediaSopa(object):

    def test_sopa_overlay(self):
        player_url = self.conf['player_url']
        self.driver.get(player_url)

        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to_frame(iframe)

        try:
            element = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, "mw-sopaOverlay"))
            )
        finally:
            sopa_overlay = self.driver.find_element_by_id("mw-sopaOverlay")

        assert sopa_overlay.text.splitlines()[0] == "Imagine a World"

    def test_sopa_overlay_js(self):
        player_url = self.conf['player_url']
        self.driver.get(player_url)

        js = open("js/wikipedia/overlay.js", 'r').read()

        txt = self.driver.execute_script(js)
        assert txt == "Imagine a World"
