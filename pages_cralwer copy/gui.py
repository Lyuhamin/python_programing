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

    def search(self):
        keyword = self.entry.get()
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

        self.display_results(keyword)

    def display_results(self, keyword):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"검색어: {keyword}\n\n")

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if self.results_joongonara:
            # (title, price, link, image_url) 형태로 언패킹합니다.
            for idx, (title, price, link, image_url) in enumerate(self.results_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n헬로마켓 결과:\n")
        if self.results_hellomarket:
            # (title, price, link, image_url) 형태로 언패킹합니다.
            for idx, (title, price, link, image_url) in enumerate(self.results_hellomarket, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        self.result_text.insert(tk.END, "\n후루츠패밀리 결과:\n")
        if self.results_fruitfamily:
            # (title, price, link, image_url) 형태로 언패킹합니다.
            for idx, (title, price, link, image_url) in enumerate(self.results_fruitfamily, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def sort_by_price(self):
        def parse_price(price_str):
            # 가격 문자열에서 숫자만 추출하고 정수로 변환합니다.
            return int(''.join(filter(str.isdigit, price_str)))

        # 모든 결과를 결합합니다. 각 결과는 (title, price, link, image_url) 형태입니다.
        combined_results = self.results_joongonara + self.results_hellomarket + self.results_fruitfamily
        # 가격순으로 정렬합니다.
        sorted_results = sorted(combined_results, key=lambda x: parse_price(x[1]))

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 결과 (낮은 가격순):\n\n")

        if sorted_results:
            for idx, (title, price, link, image_url) in enumerate(sorted_results, start=1):
                self.result_text.insert(tk.END, f"{idx}. 상품명: {title}, 가격: {price}\n링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
