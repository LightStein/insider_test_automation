import pytest
from selenium import webdriver
from config.config import get_chrome_options, CHROME_NODE_URL

@pytest.fixture(scope="module")
def driver():
    options = get_chrome_options()
    driver = webdriver.Remote(command_executor=CHROME_NODE_URL, options=options)
    if not options.headless:
        driver.maximize_window()
    yield driver
    driver.quit()
