import tkinter as tk
from tkinter import ttk
from hellomarket_crawler import HellomarketCrawler
from joongonara_crawler import JoongonaraCrawler
from fruitfamily_crawler import FruitfamilyCrawler
from danawa_crawler import DanawaCrawler

class SearchApp:
    def __init__(self, master):
        self.master = master

        master.title("중고거래 도우미")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = ttk.Button(self.frame, text="검색", command=self.search)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.sort_button = ttk.Button(self.frame, text="낮은 가격순", command=self.sort_by_price)
        self.sort_button.grid(row=0, column=2, padx=5, pady=5)

        self.result_text = tk.Text(self.frame, height=20, width=110)
        self.result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.results_joongonara = []
        self.results_hellomarket = []
        self.results_fruitfamily = []
        self.results_danawa = []

    def search(self):
        keyword = self.entry.get()
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 중...\n")

        joongonara_crawler = JoongonaraCrawler()
        hellomarket_crawler = HellomarketCrawler()
        fruitfamily_crawler = FruitfamilyCrawler()
        danawa_crawler = DanawaCrawler()

        self.results_joongonara = joongonara_crawler.crawl(keyword)
        self.results_hellomarket = hellomarket_crawler.crawl(keyword)
        self.results_fruitfamily = fruitfamily_crawler.crawl(keyword)
        self.results_danawa = danawa_crawler.crawl(keyword)

        joongonara_crawler.close()
        hellomarket_crawler.close()
        fruitfamily_crawler.close()
        danawa_crawler.close()

        self.display_results(keyword)

    def display_results(self, keyword):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"검색어: {keyword}\n\n")

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if self.results_joongonara:
            for idx, (title, price) in enumerate(self.results_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n헬로마켓 결과:\n")
        if self.results_hellomarket:
            for idx, (title, price) in enumerate(self.results_hellomarket, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n후루츠패밀리 결과:\n")
        if self.results_fruitfamily:
            for idx, (title, price) in enumerate(self.results_fruitfamily, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "다나와 결과:\n")
        if self.results_fruitfamily:
            for idx, (title, price) in enumerate(self.results_fruitfamily, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
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
            for idx, (title, price) in enumerate(sorted_results, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()
