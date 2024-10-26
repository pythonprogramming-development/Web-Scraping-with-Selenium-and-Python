import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Function to initialize the Selenium WebDriver
def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to find all elements using different strategies
def find_elements(driver, strategy, value):
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

        return wait.until(EC.presence_of_all_elements_located(locator))

    except Exception as e:
        error_message = f"Error finding elements using {strategy} with value '{value}': {e}"
        print(error_message)
        return []

# Function to scrape a webpage and export data
def scrape_website():
    driver = init_driver(headless=True)
    websiteInp = input("Enter URL for desired website to scrape: ") #exapmle : https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off
    elementInp = input("Enter the class_name of the desired element to scrape: ") #example : KzDlHZ
    export_format = input("Choose export format (CSV or JSON): ").strip().lower()

    try:
        # Open the target website
        driver.get(websiteInp)
        time.sleep(5)  # Adding a 5-second wait after loading the page

        # Find elements
        elements = find_elements(driver, "class_name", elementInp)
  # testWebsite = "https://scrapingclub.com/"
    # testElement = "w-full.rounded.border"
# exercise1_card = find_element(driver, "class_name", elementInp) # Use testElement here instead of elementInp
   # you can also use:
        # exercise1_card = find_element(driver, 'css_selector', '.w-full.rounded.border')
        # exercise1_card = find_element(driver, 'xpath', '/html/body/div[3]/div[2]/div/div[1]')
        
        # Extract and format data
        data = [{"content": el.text} for el in elements if el.text]
        
        if not data:
            print("No data found to export.")
            return

        # Export data
        if export_format == 'csv':
            with open("scraped_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["content"])
                writer.writeheader()
                writer.writerows(data)
            print("Data exported to 'scraped_data.csv'.")

        elif export_format == 'json':
            with open("scraped_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Data exported to 'scraped_data.json'.")

        else:
            print("Invalid format selected. Please choose CSV or JSON.")

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_website()
