import re
from urllib.parse import urlparse  # Import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_valid_url(url):  # Include this function
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def sanitize_locator(locator):   # Include this function
    sanitized_locator = re.sub(r"[^a-zA-Z0-9.#\[\]]", "", locator)
    return sanitized_locator

# Function to initialize the Selenium WebDriver
def init_driver(headless=True):
    # Set up Chrome options
    chrome_options = Options()

    # Enable headless mode if needed
    if headless:
        chrome_options.add_argument("--headless=new")

    # Add any other necessary options
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initializing Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to find an element using different strategies
def find_element(driver, strategy, value):
    wait = WebDriverWait(driver, 10)
    try:
        if strategy == "class_name":
            return wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif strategy == "css_selector":
            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        elif strategy == "xpath":
            return wait.until(EC.presence_of_element_located((By.XPATH, value)))
        else:
            raise ValueError(
                "Invalid strategy. Use 'class_name', 'css_selector', or 'xpath'."
            )
    except Exception as e:
        print(f"Error finding element: {e}")
        return None


# Function to scrape a webpage
def scrape_website():
    driver = init_driver(headless=True)

    while True: # loop until valid url is entered
        websiteInp = input("Enter URL for desired website to scrape: ")
         if is_valid_url(websiteInp):  
            break
        else:
            print("Invalid URL.  Please enter a valid URL.")
    
    elementInp = input("Enter the class_name (alphanumeric, ., #, [] allowed): ")
    sanitized_element = sanitize_locator(elementInp) # Sanitize the input
    # testWebsite = "https://scrapingclub.com/"
    # testElement = "w-full.rounded.border"
    try:
        # Open the target website
        driver.get(
            websiteInp
        )  # Use testWebsite variable here for texting purposes, instead of websiteInp

        # Find elements using different strategies
        exercise1_card = find_element(
            driver, "class_name", sanitized_element
        )  # Use testElement here instead of elementInp
        # you can also use:
        # exercise1_card = find_element(driver, 'css_selector', '.w-full.rounded.border')
        # exercise1_card = find_element(driver, 'xpath', '/html/body/div[3]/div[2]/div/div[1]')

        # If the element is found, print its text or other attributes
        if exercise1_card:
            print("Card content:", exercise1_card.text)
        else:
            print("Element not found.")

    except Exception as e:
        # Catch and print any errors during the scraping process
        print(f"An error occurred: {e}")

    finally:
        # Release resources and close the browser
        driver.quit()


if __name__ == "__main__":
    scrape_website()
