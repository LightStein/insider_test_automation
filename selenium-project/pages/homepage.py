from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    COMPANY_MENU = (By.XPATH, "//a[@class='nav-link dropdown-toggle' and contains(normalize-space(text()), 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[contains(@href, '/careers/') and contains(text(), 'Careers')]")

    def navigate_to_careers(self):
        self.click_element(self.COMPANY_MENU)
        self.click_element(self.CAREERS_LINK)
