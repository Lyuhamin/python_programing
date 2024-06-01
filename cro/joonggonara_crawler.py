from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

class JoongonaraCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://web.joongna.com/search?keyword="

    def crawl(self, keyword):
        url = f"{self.base_url}{keyword}"
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        items = []
        for item in soup.find_all('div', class_='item-info'):
            title = item.find('p', class_='item-title').get_text(strip=True)
            price = item.find('p', class_='item-price').get_text(strip=True)
            items.append({"제품": title, "가격": price})

        filename = "/Users/changtaeyoung/Desktop/cro/result.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["제품", "가격"])
            writer.writeheader()
            writer.writerows(items)
        return items

    def close(self):
        self.driver.quit()
