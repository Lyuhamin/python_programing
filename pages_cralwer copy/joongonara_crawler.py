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

        for item in soup.find_all('div', class_='relative'):
            title_tag = item.find('h2', class_='line-clamp-2 text-sm md:text-base text-heading')
            price_tag = item.find('div', class_='font-semibold space-s-2 mt-0.5 text-heading lg:text-lg lg:mt-1.5')
            image_tag = item.find('img', class_= 'bg-gray-300 object-cover h-full group-hover:scale-105 w-full transition duration-200 ease-in rounded-md')  # img 태그로 변경

            if title_tag and price_tag and image_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = item.find('a')['href']  # 링크는 a 태그에서 가져옴
                image_url = image_tag.get('src') if image_tag.has_attr('src') else image_tag.get('data-src', '이미지 없음')
                items.append((title, price, link, image_url))

        return items

    def close(self):
        self.driver.quit()
