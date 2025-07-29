from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

space_url = "https://neweraofcoding.quora.com/"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get(space_url)
time.sleep(3)

# Scroll to load more posts
SCROLL_PAUSE = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract posts
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

posts = []
for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.startswith("/post/") or "quora.com/post/" in href:
        full_url = "https://www.quora.com" + href if href.startswith("/") else href
        title = a_tag.get_text().strip()
        if title and full_url not in [p[1] for p in posts]:
            posts.append((title, full_url))

# Output as Markdown
markdown = "\n".join(f"- [{title}]({link})" for title, link in posts)
print(markdown)
print(f"\nTotal posts found: {len(posts)}")

# Optional: Save to file
with open("quora_space_posts.md", "w", encoding="utf-8") as f:
    f.write(markdown)
