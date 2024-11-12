import os

BASE_URL = "https://useinsider.com"
CHROME_NODE_URL = "http://chrome-node-service:4444"

HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

def get_chrome_options():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
    return options
