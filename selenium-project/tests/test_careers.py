import pytest
from pages.homepage import HomePage
from pages.careers_page import CareersPage
from config.config import BASE_URL

@pytest.mark.usefixtures("driver")
def test_careers_page_blocks(driver):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    home_page.navigate_to_careers()
    
    careers_page = CareersPage(driver)
    careers_page.verify_career_page_blocks()
