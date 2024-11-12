from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CareersPage(BasePage):
    LOCATIONS_BLOCK = (By.XPATH, "//ul[@class='glide__slides']//li[*]//div//img[not(@alt='')]")
    TEAM_BLOCK = (By.XPATH, "//section[contains(@id, 'career')]//div[contains(@class,'job-item')]")
    LIFE_AT_INSIDER_BLOCK = (By.XPATH, "//div[@class='elementor-carousel-image']")

    def verify_career_page_blocks(self):
        assert len(self.driver.find_elements(*self.LOCATIONS_BLOCK)) > 4, "Locations block content is not visible"
        assert len(self.driver.find_elements(*self.TEAM_BLOCK)) == 3, "Teams block content is not visible"
        assert len(self.driver.find_elements(*self.LIFE_AT_INSIDER_BLOCK)) > 2, "Life at Insider block content is not visible"
