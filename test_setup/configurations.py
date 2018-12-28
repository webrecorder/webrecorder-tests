"""Module containing test setup methods"""
from selenium.webdriver.remote.webdriver import WebDriver

__all__ = ["set_selenium_driver_timeouts"]


def set_selenium_driver_timeouts(driver: WebDriver) -> None:
    """Sets the script execution timeout to 90 seconds and the
    page load timeout to 60 seconds
    """
    driver.set_script_timeout(90)
    driver.set_page_load_timeout(60)
