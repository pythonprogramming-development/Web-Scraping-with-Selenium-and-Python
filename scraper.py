import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging for better traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InvalidStrategyError(Exception):
    """Custom exception for invalid element strategy."""
    pass

# Function to initialize the Selenium WebDriver
def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    logging.info("WebDriver initialized successfully.")
    return driver

# Function to find an element using different strategies
def find_element(driver, strategy, value):
    wait = WebDriverWait(driver, 10)
    try:
        # Dynamically fetch the strategy from the By class
        by_strategy = getattr(By, strategy.upper(), None)
        if by_strategy is None:
            raise InvalidStrategyError(f"Invalid strategy: '{strategy}'. Use 'id', 'name', 'class_name', 'css_selector', 'xpath', etc.")

        element = wait.until(EC.presence_of_element_located((by_strategy, value)))
        logging.info(f"Element found using strategy: {strategy}")
        return element

    except TimeoutException:
        logging.error("Timeout: Element not found.")
    except NoSuchElementException:
        logging.error("No such element found.")
    except InvalidStrategyError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None

# Function to scrape a webpage
def scrape_website():
    # Allow user to choose headless mode
    headless_mode = input("Run in headless mode? (yes/no): ").strip().lower() == "yes"
    driver = init_driver(headless=headless_mode)
    
    website_url = input("Enter URL for the website to scrape: ").strip()
    strategy = input("Enter the search strategy (e.g., id, name, class_name, css_selector, xpath): ").strip()
    identifier = input("Enter the identifier for the desired element: ").strip()

    try:
        driver.get(website_url)
        logging.info(f"Accessing {website_url}")
        
        element = find_element(driver, strategy, identifier)
        if element:
            print("Element content:", element.text)
        else:
            print("Element not found.")
            logging.warning("Scraping failed due to missing element.")
            
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
    finally:
        driver.quit()
        logging.info("WebDriver closed.")

if __name__ == "__main__":
    scrape_website()
