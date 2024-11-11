from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
import os
from selenium.common.exceptions import TimeoutException

# Initialize the WebDriver globally
options = webdriver.ChromeOptions()
headless = os.getenv('HEADLESS', 'false').lower() == 'true'

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Base URL
BASE_URL = "https://useinsider.com"

@pytest.fixture(scope="module")
def setup():
    global driver
    # Maximize the browser window and navigate to the base URL
    driver.maximize_window()
    driver.get(BASE_URL)
    yield
    driver.quit()

def wait_for_jquery(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: driver.execute_script("return jQuery.active == 0;")
        )
        print("All jQuery Ajax requests have completed.")
    except TimeoutException:
        print("Timed out waiting for jQuery to finish.")

# Test 1: Check if Insider homepage is opened
def test_homepage_opened(setup):
    assert "Insider" in driver.title, "Home page not opened"
    
# Test 2: Check Career page, its blocks - Locations, Teams, Life at Insider
def test_navigate_to_careers_page():
    # Select "Company" menu and then "Careers"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='nav-link dropdown-toggle' and contains(normalize-space(text()), 'Company')]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/careers/') and contains(text(), 'Careers')]"))).click()
    
    # Verify Career page elements
    assert "careers" in driver.current_url, "Career page is not opened"
    
    # Verify blocks are visible on Career page
    locations_block_items = driver.find_elements(By.XPATH, "//ul[@class='glide__slides']//li[*]//div//img[not(@alt='')]")
    team_block_items = driver.find_elements(By.XPATH, "//section[contains(@id, 'career')]//div[contains(@class,'job-item')]")
    life_at_insider_block_items = driver.find_elements(By.XPATH, "//div[@class='elementor-carousel-image']")
    
    assert len(locations_block_items) > 4, "Locations block content is not visible"
    assert len(team_block_items) == 3, "Teams block content is not visible"
    assert len(life_at_insider_block_items) > 2, "Life at Insider block content is not visible"

# Test 3: Go to QA careers, filter jobs by Location - Istanbul, Turkey and department - Quality Assurance
def test_filter_qa_jobs():
    # Go to QA careers
    driver.get(BASE_URL + "/careers/quality-assurance/")
    
    # Click "See all QA jobs"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "See all QA jobs"))).click()

    wait_for_jquery(driver)
    
    # Manually choose department if it is not automatically selected
    try:
        WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.ID, "select2-filter-by-department-container"), "Quality Assurance"))
    except:
        department_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "select2-filter-by-department-container")))
        department_dropdown.click()
        qa_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Quality Assurance')]")))
        qa_option.click()

    print("##################### Before Click Filter #######################")
    # Filter jobs by Location
    wait = WebDriverWait(driver, 10)
    location_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container")))
    location_dropdown.click()
    print("##################### Click Filter #######################")

    # Wait for a short period to check if the list is loaded
    time.sleep(2)
    
    # If the list is not loaded, click the dropdown to hide it and then click again
    if not driver.find_elements(By.XPATH, "//li[contains(text(), 'Istanbul, Turkey')]"):
        location_dropdown.click()  # Hide dropdown
        time.sleep(1)
        location_dropdown.click()  # Show dropdown again
    
    # Select Istanbul, Turkey
    istanbul_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Istanbul, Turkey')]")))
    istanbul_option.click()

    # Check that job list is present
    jobs_list = driver.find_elements(By.CLASS_NAME, "position-list-item-wrapper")

    time.sleep(5)
    assert len(jobs_list) > 0, "No jobs found for the given filters"

# Test 4: Verify job details contain "Quality Assurance" and "Istanbul, Turkey"
def test_check_job_details():
    jobs_list = driver.find_elements(By.CLASS_NAME, "position-list-item-wrapper")
    print(jobs_list)
    
    for job in jobs_list:
        position = job.find_element(By.CLASS_NAME, "position-title").text
        department = job.find_element(By.CLASS_NAME, "position-department").text
        location = job.find_element(By.CLASS_NAME, "position-location").text
        
        assert "Quality Assurance" in position, "Job Position does not contain 'Quality Assurance'"
        assert "Quality Assurance" in department, "Job Department does not contain 'Quality Assurance'"
        assert "Istanbul, Turkey" in location, "Job Location does not contain 'Istanbul, Turkey'"
        print("##################### Check Done #######################")

# Test 5: Click "View Role" button and check Lever Application form page
def test_view_role_and_lever_page():
    jobs_list = driver.find_elements(By.CLASS_NAME, "position-list-item-wrapper")
    assert len(jobs_list) > 0, "No job items found"
    
    # Hover over the job item to reveal the "View Role" button
    webdriver.ActionChains(driver).move_to_element(jobs_list[0]).perform()
    view_role_button = jobs_list[0].find_element(By.LINK_TEXT, "View Role")
    assert view_role_button.is_displayed(), "'View Role' button is not displayed"
    view_role_button.click()
    
    # Switch to the new tab and verify Lever application form
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.url_contains("lever.co"))
    assert "lever.co" in driver.current_url, "Not redirected to Lever application form page"
    
    # Close the tab and switch back to the original window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    pytest.main()
