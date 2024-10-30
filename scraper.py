import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def find_elements(driver, strategy, value):
    wait = WebDriverWait(driver, 10)
    try:
        by_strategy = getattr(By, strategy.upper(), None)
        if not by_strategy:
            raise ValueError(f"Invalid strategy '{strategy}'. Supported strategies include 'id', 'name', 'class_name', 'css_selector', 'xpath', etc.")
        
        return wait.until(EC.presence_of_all_elements_located((by_strategy, value)))
    
    except Exception as e:
        print(f"Error finding elements using '{strategy}' with value '{value}': {e}")
        return []

def extract_text_content(elements):
    data = []
    for el in elements:
        if el.text.strip():
            soup = BeautifulSoup(el.get_attribute('outerHTML'), 'html.parser')
            data.append({"content": soup.get_text(strip=True)})
    return data

# (CSV or JSON)
def export_data(data, format_choice):
    if not data:
        print("No data available to export.")
        return
    
    try:
        if format_choice == 'csv':
            with open("scraped_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["content"])
                writer.writeheader()
                writer.writerows(data)
            print("Data successfully exported to 'scraped_data.csv'.")
        
        elif format_choice == 'json':
            with open("scraped_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Data successfully exported to 'scraped_data.json'.")
        else:
            print("Invalid format selected. Please choose CSV or JSON.")
    
    except IOError as e:
        print(f"File I/O error during export: {e}")

def scrape_website():
    driver = init_driver(headless=True)
    website_url = input("Enter URL for the desired website to scrape: ").strip()
    strategy = input("Enter the strategy (e.g., id, name, class_name, css_selector, xpath): ").strip().lower()
    identifier = input("Enter the value of the identifier to locate the element: ").strip()
    
    # Validate and loop for valid export format
    export_format = ""
    while export_format not in ["csv", "json"]:
        export_format = input("Choose export format (CSV or JSON): ").strip().lower()
        if export_format not in ["csv", "json"]:
            print("Invalid format. Please enter 'CSV' or 'JSON'.")

    try:
        # Open the target website and dynamically wait for content
        driver.get(website_url)
        
        # Locate elements
        elements = find_elements(driver, strategy, identifier)
        
        # Extract data
        data = extract_text_content(elements)
        
        # Export data
        export_data(data, export_format)
    
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_website()
