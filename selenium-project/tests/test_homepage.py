import pytest
from pages.homepage import HomePage
from config.config import BASE_URL

@pytest.mark.usefixtures("driver")
def test_homepage_opened(driver):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    assert "Insider" in driver.title, "Home page not opened"
