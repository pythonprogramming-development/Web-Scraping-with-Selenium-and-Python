from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver(headless=True):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def find_element(driver, strategy, value):
    wait = WebDriverWait(driver, 10)
    try:
        # Dynamically fetch the strategy from the By class
        by_strategy = getattr(By, strategy.upper(), None)
        
        if by_strategy is None:
            raise ValueError(f"Invalid strategy: '{strategy}'. Please use a valid strategy from the By class.")

        return wait.until(EC.presence_of_element_located((by_strategy, value)))

    except Exception as e:
        print(f"Error finding element: {e}")
        return None


def scrape_website():
    driver = init_driver(headless=True)
    websiteInp = input("Enter URL for desired website to scrape: ")
    elementInp = input("Enter the class_name of the desired element to scrape: ")

    try:
        driver.get(websiteInp)

        exercise1_card = find_element(driver, "class_name", elementInp)

        if exercise1_card:
            print("Card content:", exercise1_card.text)
        else:
            print("Element not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_website()
