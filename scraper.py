from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            locator = (By.CLASS_NAME, value)
        elif strategy == "css_selector":
            locator = (By.CSS_SELECTOR, value)
        elif strategy == "xpath":
            locator = (By.XPATH, value)
        else:
            raise ValueError(
                f"Invalid strategy '{strategy}'. Use 'class_name', 'css_selector', or 'xpath'."
            )

        return wait.until(EC.presence_of_element_located(locator))

    except Exception as e:
        error_message = f"Error finding element using {strategy} with value '{value}': {e}"
        print(error_message)
        raise

# Function to scrape a webpage
def scrape_website():
    driver = init_driver(headless=True)
    websiteInp = input("Enter URL for desired website to scrape: ")
    elementInp = input("Enter the class_name of the desired element to scrape: ")
    # testWebsite = "https://scrapingclub.com/"
    # testElement = "w-full.rounded.border"
    try:
        # Open the target website
        driver.get(
            websiteInp
        )  # Use testWebsite variable here for texting purposes, instead of websiteInp

        # Find elements using different strategies
        exercise1_card = find_element(driver, "class_name", elementInp) # Use testElement here instead of elementInp
        # you can also use:
        # exercise1_card = find_element(driver, 'css_selector', '.w-full.rounded.border')
        # exercise1_card = find_element(driver, 'xpath', '/html/body/div[3]/div[2]/div/div[1]')

        # If the element is found, print its text or other attributes
        if exercise1_card:
            print("Card content:", exercise1_card.text)
        else:
            print("Element not found.")

    except ValueError as e: # handle specifically invalid strategy provided by user
        print(e)
    except Exception as e: # Handles other exceptions from find_element (like TimeoutException)
        pass # No need to print here as find_element already did.

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_website()
