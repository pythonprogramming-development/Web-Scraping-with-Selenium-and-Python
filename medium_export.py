import requests
import xml.etree.ElementTree as ET

rss_url = "https://medium.com/feed/@eraoftech"
resp = requests.get(rss_url)
resp.raise_for_status()

root = ET.fromstring(resp.content)
ns = {'m': 'http://purl.org/rss/1.0/modules/content/'}

links = []
for item in root.findall('./channel/item'):
    title = item.findtext('title')
    link = item.findtext('link')
    links.append((title, link))

print("\n".join(f"- [{title}]({link})" for title, link in links))
print(f"\nTotal posts found in feed: {len(links)}")
