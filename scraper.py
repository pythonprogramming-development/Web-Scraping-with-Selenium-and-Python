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

    # Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# scraping a webpage
def scrape_website():
    driver = init_driver(headless=True)
    
    try:
        # Open the target website
        driver.get('https://scrapingclub.com/')
        
        # Wait for the element to be present before interacting with it
        wait = WebDriverWait(driver, 10)
        
        # Adjust the selector based on your requirement
        exercise1_card = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'w-full.rounded.border')))
        
        # If the element is found, print its text or other attributes
        print("Card content:", exercise1_card.text)
        
    except Exception as e:
        # Catch and print any errors during the scraping process
        print(f"An error occurred: {e}")
    
    finally:
        # Release resources and close the browser
        driver.quit()

if __name__ == "__main__":
    scrape_website()
