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
        chrome_options.add_argument('--headless=new')
    
    # Add any other necessary options
    chrome_options.add_argument('--disable-gpu') 
    chrome_options.add_argument('--no-sandbox') 
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initializing Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to find an element using different strategies
def find_element(driver, strategy, value):
    wait = WebDriverWait(driver, 10)
    try:
        if strategy == 'class_name':
            return wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif strategy == 'css_selector':
            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        elif strategy == 'xpath':
            return wait.until(EC.presence_of_element_located((By.XPATH, value)))
        else:
            raise ValueError("Invalid strategy. Use 'class_name', 'css_selector', or 'xpath'.")
    except Exception as e:
        print(f"Error finding element: {e}")
        return None

# Function to scrape content from the current page
def scrape_current_page(driver):
    try:
        exercise1_card = find_element(driver, 'class_name', 'w-full.rounded.border')
        if exercise1_card:
            print("Card content:", exercise1_card.text)
        else:
            print("Element not found.")
    except Exception as e:
        print(f"Error scraping page: {e}")

# Function to handle pagination
def handle_pagination(driver):
    while True:
        try:
            # Scrape the current page
            scrape_current_page(driver)

            # Find the "Next" button and click it if it exists
            next_button = find_element(driver, 'xpath', '//a[@rel="next"]')
            if next_button:
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(next_button))  # Wait until the next page loads
            else:
                print("No more pages to scrape.")
                break  # Exit the loop if there's no next button
        except Exception as e:
            print(f"Error navigating pages: {e}")
            break

# Function to scrape a website with pagination
def scrape_website():
    driver = init_driver(headless=True)
    
    try:
        # Open the target website
        driver.get('https://scrapingclub.com/')
        
        # Scrape the first page and handle pagination
        handle_pagination(driver)
        
    except Exception as e:
        # Catch and print any errors during the scraping process
        print(f"An error occurred: {e}")
    
    finally:
        # Release resources and close the browser
        driver.quit()

if __name__ == "__main__":
    scrape_website()
