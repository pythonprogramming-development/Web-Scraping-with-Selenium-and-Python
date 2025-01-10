# from selenium import webdriver 
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# # initialize an instance of the chrome driver (browser)
# driver = webdriver.Chrome()


# # enable headless mode in Selenium
# options = Options()
# # enable headless mode
# options.headless = True

# options.add_argument('--headless=new')

# driver = webdriver.Chrome(
#     options=options, 
#     # other properties...
# )

# # visit your target site
# driver.get('https://scrapingclub.com/')

# # scraping logic...
# exercise1_card = driver.find_element(By.CLASS_NAME, 'w-full.rounded.border') #w-full rounded border
# # or
# # exercise1_card = driver.find_element(By.CSS_SELECTOR, '.w-full.rounded.border')
# # or
# # exercise1_card = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]')

# print(exercise1_card)
# # release the resources allocated by Selenium and shut down the browser
# driver.quit()

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# initialize an instance of the chrome driver (browser)
options = Options()
options.headless = True
options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options)

try:
    # visit your target site
    driver.get('https://scrapingclub.com/')

    # wait for the element to be present
    wait = WebDriverWait(driver, 10)
    exercise1_card = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'w-full.rounded.border')))
    
    print(exercise1_card.text)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # release the resources allocated by Selenium and shut down the browser
    driver.quit()