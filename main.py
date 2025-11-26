# main.py 코드 (Selenium RSS 생성기)
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

TARGET_URL = "https://game.naver.com/lounge/Tree_Of_Savior_Neverland/board/3"
OUTPUT_FILE = "feed.xml"

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_articles():
    driver = get_driver()
    driver.get(TARGET_URL)
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    article_elements = soup.select("a.ArticleListItem_link__Y0kPu")
    articles = []

    for item in article_elements[:20]:
        title_elem = item.select_one(".ArticleContent_title__j9WGr")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link = "https://game.naver.com" + item["href"]
        pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")
        articles.append({"title": title, "link": link, "pubDate": pub_date})
    return articles

def generate_rss(items):
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Naver TOS Neverland Board 3 (Unofficial RSS)</title>
<link>{TARGET_URL}</link>
<description>Auto-generated RSS feed</description>
"""
    for item in items:
        rss += f"""
<item>
<title>{item['title']}</title>
<link>{item['link']}</link>
<pubDate>{item['pubDate']}</pubDate>
</item>
"""
    rss += "</channel></rss>"
    return rss

def main():
    items = fetch_articles()
    rss = generate_rss(items)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    print("RSS generated:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
