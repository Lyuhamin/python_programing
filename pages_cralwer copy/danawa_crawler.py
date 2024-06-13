from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class DanawaCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://www.danawa.com/"

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        time.sleep(5)  # 페이지 로딩을 위한 대기 시간 추가

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []

        for item in soup.find_all('div', class_='prod_main_info'):  # 실제 HTML 구조에 맞게 수정 필요
            title_tag = item.find('div', class_='prod_name')  # 실제 HTML 구조에 맞게 수정 필요
            price_tag = item.find('div', class_='click_log_product_standard_price_')  # 실제 HTML 구조에 맞게 수정 필요

            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                items.append((title, price))

        return items

    def close(self):
        self.driver.quit()