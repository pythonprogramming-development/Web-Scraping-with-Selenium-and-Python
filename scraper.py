from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome()


# enable headless mode in Selenium
options = Options()
# enable headless mode
options.headless = True

options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options, 
    # other properties...
)

# visit your target site
driver.get('https://scrapingclub.com/')

# scraping logic...
exercise1_card = driver.find_element(By.CLASS_NAME, 'w-full.rounded.border')
# or
exercise1_card = driver.find_element(By.CSS_SELECTOR, '.w-full.rounded.border')
# or
exercise1_card = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]')

print(exercise1_card)
# release the resources allocated by Selenium and shut down the browser
# driver.quit()
