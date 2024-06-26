from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class HellomarketCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://www.hellomarket.com/search?q="

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩을 위한 대기 시간 추가

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []

        for item in soup.find_all('div', class_='sc-2e746fd3-0 loRRgN'):
            title_tag = item.find('div', class_='sc-2e746fd3-5 RmlFc')
            price_tag = item.find('div', class_='sc-2e746fd3-5 laAErS')
            image_tag = item.find('img', class_='sc-b34a2ec2-0 bOxxOH')
            link_tag = item.find('a')

            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                
                # link_tag가 None이 아닌지 확인하고 링크 구성
                if link_tag and link_tag.get('href'):
                    link = link_tag['href']
                    # 링크가 상대 경로일 경우 절대 경로로 변환
                    if not link.startswith('http'):
                        link = f"https://www.hellomarket.com{link}"
                else:
                    link = '링크 없음'

                # image_tag가 None이 아닌지 확인하고 이미지 URL 구성
                if image_tag:
                    image_url = image_tag.get('src') if image_tag.has_attr('src') else image_tag.get('data-src', '이미지 없음')
                else:
                    image_url = '이미지 없음'

                items.append((title, price, link, image_url))

        return items

    def close(self):
        self.driver.quit()
