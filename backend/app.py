from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

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

@app.route('/api/scrape', methods=['POST'])
def scrape_website():
    try:
        data = request.json
        website_url = data.get('url')
        element_selector = data.get('selector')
        selector_type = data.get('selectorType', 'class_name')
        
        if not website_url or not element_selector:
            return jsonify({'error': 'Missing required parameters'}), 400

        driver = init_driver(headless=True)
        
        try:
            driver.get(website_url)
            time.sleep(5)

            elements = find_elements(driver, selector_type, element_selector)
            scraped_data = [{"content": el.text} for el in elements if el.text]
            
            if not scraped_data:
                return jsonify({'error': 'No data found'}), 404

            return jsonify({
                'status': 'success',
                'data': scraped_data
            })

        finally:
            driver.quit()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)