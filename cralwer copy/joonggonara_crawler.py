# joongonara_crawler.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class JoongonaraCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://web.joongna.com/search?keyword="

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        time.sleep(5)  # 페이지 로딩을 위한 대기 시간 추가

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []
        print(f"Crawling URL: {url}")  # URL 출력
        print(f"Page title: {self.driver.title}")  # 페이지 타이틀 출력

        for item in soup.find_all('div', class_='relative'):
            title_tag = item.find('div', class_='w-full overflow-hidden p-2 md:px-2.5 xl:px-4')
            price_tag = item.find('div', class_='font-semibold space-s-2 mt-0.5 text-heading lg:text-lg lg:mt-1.5')
            link_tag = item.find('a', class_='group box-border overflow-hidden flex rounded-md cursor-pointer pe-0 pb-2 lg:pb-3 flex-col items-start transition duration-200 ease-in-out transform bg-white')

            if title_tag and price_tag and link_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = "https://web.joongna.com" + link_tag['href']
                items.append((title, price, link))
                print(f"Found item: {title} - {price} - {link}")  # 찾은 아이템 출력

        return items

    def close(self):
        self.driver.quit()
