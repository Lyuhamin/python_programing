import tkinter as tk
from tkinter import ttk
from hellomarket_crawler import HellomarketCrawler
from joongonara_crawler import JoongonaraCrawler
from fruitfamily_crawler import FruitfamilyCrawler

class SearchApp:
    def __init__(self, master):
        self.master = master

        master.title("중고거래 도우미")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 검색어 입력
        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        # 검색 버튼
        self.search_button = ttk.Button(self.frame, text="검색", command=self.search)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        # 낮은 가격순 버튼
        self.sort_button = ttk.Button(self.frame, text="낮은 가격순", command=self.sort_by_price)
        self.sort_button.grid(row=0, column=2, padx=5, pady=5)

        # 최소 가격 입력
        self.min_price_label = ttk.Label(self.frame, text="최소 가격:")
        self.min_price_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.min_price_entry = ttk.Entry(self.frame, width=20)
        self.min_price_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        # 최대 가격 입력
        self.max_price_label = ttk.Label(self.frame, text="최대 가격:")
        self.max_price_label.grid(row=1, column=2, sticky=tk.W, padx=5)
        self.max_price_entry = ttk.Entry(self.frame, width=20)
        self.max_price_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)

        # 결과 출력 영역
        self.result_text = tk.Text(self.frame, height=20, width=110)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.results_joongonara = []
        self.results_hellomarket = []
        self.results_fruitfamily = []

    def search(self):
        keyword = self.entry.get()
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 중...\n")

        # 최소 및 최대 가격 필드의 값 가져오기
        min_price = self.min_price_entry.get()
        max_price = self.max_price_entry.get()
        min_price = int(min_price) if min_price.isdigit() else 0
        max_price = int(max_price) if max_price.isdigit() else float('inf')

        joongonara_crawler = JoongonaraCrawler()
        hellomarket_crawler = HellomarketCrawler()
        fruitfamily_crawler = FruitfamilyCrawler()

        self.results_joongonara = joongonara_crawler.crawl(keyword)
        self.results_hellomarket = hellomarket_crawler.crawl(keyword)
        self.results_fruitfamily = fruitfamily_crawler.crawl(keyword)

        joongonara_crawler.close()
        hellomarket_crawler.close()
        fruitfamily_crawler.close()

        # 가격 필터링 적용
        self.results_joongonara = self.filter_by_price(self.results_joongonara, min_price, max_price)
        self.results_hellomarket = self.filter_by_price(self.results_hellomarket, min_price, max_price)
        self.results_fruitfamily = self.filter_by_price(self.results_fruitfamily, min_price, max_price)

        self.display_results(keyword)

    def filter_by_price(self, results, min_price, max_price):
        filtered_results = []
        for title, price, link, image_url in results:
            price_value = int(''.join(filter(str.isdigit, price)))
            if min_price <= price_value <= max_price:
                filtered_results.append((title, price, link, image_url))
        return filtered_results

    def display_results(self, keyword):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"검색어: {keyword}\n\n")

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if self.results_joongonara:
            for idx, (title, price, link, image_url) in enumerate(self.results_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}, 링크: {link}, 이미지: {image_url}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n헬로마켓 결과:\n")
        if self.results_hellomarket:
            for idx, (title, price, link, image_url) in enumerate(self.results_hellomarket, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}, 링크: {link}, 이미지: {image_url}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n후루츠패밀리 결과:\n")
        if self.results_fruitfamily:
            for idx, (title, price, link, image_url) in enumerate(self.results_fruitfamily, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}, 링크: {link}, 이미지: {image_url}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def sort_by_price(self):
        def parse_price(price_str):
            # 가격 문자열에서 숫자만 추출하고 정수로 변환합니다.
            return int(''.join(filter(str.isdigit, price_str)))

        combined_results = self.results_joongonara + self.results_hellomarket + self.results_fruitfamily
        sorted_results = sorted(combined_results, key=lambda x: parse_price(x[1]))  # 가격순으로 정렬

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 결과 (낮은 가격순):\n\n")

        if sorted_results:
            for idx, (title, price, link, image_url) in enumerate(sorted_results, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}, 링크: {link}, 이미지: {image_url}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()
