from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

class BunjangCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://m.bunjang.co.kr/search/products?order=accuracy&q="

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []
        for item in soup.find_all('div', class_='sc-fzXfPq'):
            title = item.find('p', class_='sc-tilXH').get_text(strip=True)
            price = item.find('p', class_='sc-kgoBCf').get_text(strip=True)
            items.append({"제품": title, "가격": price})
                # 검색 결과를 CSV 파일로 저장
        filename = "/Users/changtaeyoung/Desktop/cro/result.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["제품", "가격"])
            writer.writeheader()
            writer.writerows(items)
        
        return items

    def close(self):
        self.driver.quit()

