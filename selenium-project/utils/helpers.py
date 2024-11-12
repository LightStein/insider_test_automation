from selenium.webdriver.support.ui import WebDriverWait

def wait_for_jquery(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: driver.execute_script("return jQuery.active == 0;")
        )
    except TimeoutException:
        print("Timed out waiting for jQuery to finish.")
