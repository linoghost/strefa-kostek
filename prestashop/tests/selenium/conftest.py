import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


@pytest.fixture(scope="function")
def driver():
    """
    Fixture do inicjalizacji i sprzątania webdrivera Chrome
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment dla trybu bez GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    """
    URL localhost dla PrestaShopa
    """
    return "http://localhost"
