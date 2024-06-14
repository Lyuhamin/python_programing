from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class DanawaCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://search.danawa.com/dsearch.php?query="

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        time.sleep(5)  # 페이지 로딩을 위한 대기 시간 추가

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []

        for item in soup.find_all('div', class_='prod_main_info'):
            title_tag = item.find('a', class_='click_log_product_standard_title_')
            price_tag = item.find('span', class_='price_sect')
            image_tag = item.find('img', class_='thumb_link click_log_product_standard_img_')

            if title_tag and price_tag and image_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = title_tag.get('href', '링크 없음')  # get을 사용하여 href 속성이 없을 경우 기본값 설정
                image_url = image_tag.get('src') if image_tag.has_attr('src') else image_tag.get('data-src', '이미지 없음')
                items.append((title, price, link, image_url))

        return items

    def close(self):
        self.driver.quit()
