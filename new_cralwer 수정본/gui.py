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

        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.search_button = ttk.Button(self.frame, text="검색", command=self.search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.min_price_label = ttk.Label(self.frame, text="최소 가격:")
        self.min_price_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.min_price_entry = ttk.Entry(self.frame, width=20)
        self.min_price_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.max_price_label = ttk.Label(self.frame, text="최대 가격:")
        self.max_price_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        self.max_price_entry = ttk.Entry(self.frame, width=20)
        self.max_price_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        self.sort_button = ttk.Button(self.frame, text="낮은 가격순", command=self.sort_by_price)
        self.sort_button.grid(row=0, column=3, padx=5, pady=5)

        self.result_text = tk.Text(self.frame, height=20, width=110)
        self.result_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        self.results_joongonara = []
        self.results_hellomarket = []
        self.results_fruitfamily = []
        self.original_results = {'joongonara': [], 'hellomarket': [], 'fruitfamily': []}  # 원래 결과 저장
        self.sorted = False  # 현재 정렬 상태
        self.min_price = None
        self.max_price = None

    def search(self):
        keyword = self.entry.get()
        min_price_str = self.min_price_entry.get()
        max_price_str = self.max_price_entry.get()
        self.min_price = int(min_price_str) if min_price_str.isdigit() else None
        self.max_price = int(max_price_str) if max_price_str.isdigit() else None
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 중...\n")

        joongonara_crawler = JoongonaraCrawler()
        hellomarket_crawler = HellomarketCrawler()
        fruitfamily_crawler = FruitfamilyCrawler()

        self.results_joongonara = joongonara_crawler.crawl(keyword)
        self.results_hellomarket = hellomarket_crawler.crawl(keyword)
        self.results_fruitfamily = fruitfamily_crawler.crawl(keyword)

        joongonara_crawler.close()
        hellomarket_crawler.close()
        fruitfamily_crawler.close()

        self.original_results = {
            'joongonara': self.results_joongonara,
            'hellomarket': self.results_hellomarket,
            'fruitfamily': self.results_fruitfamily
        }

        self.display_results(keyword)

    def display_results(self, keyword):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"검색어: {keyword}\n\n")

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        self.display_filtered_results(self.results_joongonara)

        self.result_text.insert(tk.END, "\n헬로마켓 결과:\n")
        self.display_filtered_results(self.results_hellomarket)

        self.result_text.insert(tk.END, "\n후루츠패밀리 결과:\n")
        self.display_filtered_results(self.results_fruitfamily)

    def display_filtered_results(self, results):
        def parse_price(price_str):
            return int(''.join(filter(str.isdigit, price_str)))

        if results:
            filtered_results = []
            for title, price in results:
                price_value = parse_price(price)
                if (self.min_price is None and self.max_price is None) or \
                   (self.min_price is not None and self.max_price is None and price_value >= self.min_price) or \
                   (self.min_price is None and self.max_price is not None and self.max_price * 0.3 <= price_value <= self.max_price) or \
                   (self.min_price is not None and self.max_price is not None and self.min_price <= price_value <= self.max_price):
                    filtered_results.append((title, price))
            if filtered_results:
                for idx, (title, price) in enumerate(filtered_results, start=1):
                    self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
            else:
                self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def sort_by_price(self):
        if self.sorted:
            self.sorted = False
            self.display_results_sorted(self.original_results)
            self.sort_button.config(text="낮은 가격순")
        else:
            self.sorted = True
            self.sort_button.config(text="원래 순서로")
            def parse_price(price_str):
                return int(''.join(filter(str.isdigit, price_str)))

            combined_results = self.results_joongonara + self.results_hellomarket + self.results_fruitfamily
            sorted_results = sorted(combined_results, key=lambda x: parse_price(x[1]))
            self.display_sorted_results(sorted_results)

    def display_sorted_results(self, results):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 결과 (낮은 가격순):\n\n")

        if results:
            filtered_results = []
            def parse_price(price_str):
                return int(''.join(filter(str.isdigit, price_str)))

            for title, price in results:
                price_value = parse_price(price)
                if (self.min_price is None and self.max_price is None) or \
                   (self.min_price is not None and self.max_price is None and price_value >= self.min_price) or \
                   (self.min_price is None and self.max_price is not None and self.max_price * 0.3 <= price_value <= self.max_price) or \
                   (self.min_price is not None and self.max_price is not None and self.min_price <= price_value <= self.max_price):
                    filtered_results.append((title, price))
            
            if filtered_results:
                for idx, (title, price) in enumerate(filtered_results, start=1):
                    self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n")
            else:
                self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def display_results_sorted(self, original_results):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 결과:\n\n")

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        self.display_filtered_results(original_results['joongonara'])

        self.result_text.insert(tk.END, "\n헬로마켓 결과:\n")
        self.display_filtered_results(original_results['hellomarket'])

        self.result_text.insert(tk.END, "\n후루츠패밀리 결과:\n")
        self.display_filtered_results(original_results['fruitfamily'])

    def on_closing(self):
        self.master.destroy()

root = tk.Tk()
app = SearchApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
