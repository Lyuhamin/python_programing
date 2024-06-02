import tkinter as tk
from tkinter import ttk, scrolledtext
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler

class SearchApp:
    def __init__(self, master):
        self.master = master
        master.title("중고거래 도우미")
        master.geometry("1000x800")  # 창 크기를 더 크게 조정

        self.crawler_bunjang = BunjangCrawler()
        self.crawler_joongonara = JoongonaraCrawler()

        # 검색 및 필터 설정 프레임
        self.search_frame = ttk.Frame(master, padding="10")
        self.search_frame.pack(fill=tk.X)

        # 검색어 입력
        self.keyword_label = ttk.Label(self.search_frame, text="검색어:", font=('Arial', 14))
        self.keyword_label.pack(side=tk.LEFT, padx=5)
        
        self.keyword_entry = ttk.Entry(self.search_frame, font=('Arial', 14), width=20)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        # 최소 가격 설정
        self.min_price_label = ttk.Label(self.search_frame, text="최소 가격:", font=('Arial', 14))
        self.min_price_label.pack(side=tk.LEFT, padx=5)
        
        self.min_price_entry = ttk.Entry(self.search_frame, font=('Arial', 14), width=10)
        self.min_price_entry.pack(side=tk.LEFT, padx=5)

        # 최대 가격 설정
        self.max_price_label = ttk.Label(self.search_frame, text="최대 가격:", font=('Arial', 14))
        self.max_price_label.pack(side=tk.LEFT, padx=5)
        
        self.max_price_entry = ttk.Entry(self.search_frame, font=('Arial', 14), width=10)
        self.max_price_entry.pack(side=tk.LEFT, padx=5)

        # 검색 버튼
        self.search_button = ttk.Button(self.search_frame, text="검색", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT, padx=20)

        # 결과 출력 프레임
        self.result_frame = ttk.Frame(master, padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        # 스크롤 가능한 텍스트 상자
        self.result_text = scrolledtext.ScrolledText(self.result_frame, height=35, width=70, wrap=tk.WORD, font=('Arial', 12))
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def perform_search(self):
        keyword = self.keyword_entry.get()
        min_price = self.min_price_entry.get()
        max_price = self.max_price_entry.get()
        
        # 입력값 검증 및 변환
        try:
            min_price = max(int(min_price), 0) if min_price.isdigit() else 0
            max_price = int(max_price) if max_price.isdigit() else float('inf')
        except ValueError:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "가격 입력이 잘못되었습니다.\n")
            return
        
        # 크롤링 결과 수집
        results_bunjang = self.crawler_bunjang.crawl(keyword)
        results_joongonara = self.crawler_joongonara.crawl(keyword)

        # 결과 필터링
        filtered_results_bunjang = [item for item in results_bunjang if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
        filtered_results_joongonara = [item for item in results_joongonara if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]

        # 결과 표시
        self.display_results(filtered_results_bunjang, filtered_results_joongonara)

    def display_results(self, results_bunjang, results_joongonara):
        self.result_text.delete('1.0', tk.END)
        
        if not results_joongonara and not results_bunjang:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")
            return

        # 중고나라 결과 정렬 및 출력
        if results_joongonara:
            sorted_joongonara = sorted(results_joongonara, key=lambda x: int(x[1].replace(',', '').replace('원', '')))
            self.result_text.insert(tk.END, "중고나라 결과:\n")
            for idx, (title, price, link) in enumerate(sorted_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")

        # 번개장터 결과 정렬 및 출력
        if results_bunjang:
            sorted_bunjang = sorted(results_bunjang, key=lambda x: int(x[1].replace(',', '').replace('원', '')))
            self.result_text.insert(tk.END, "\n번개장터 결과:\n")
            for idx, (title, price, link) in enumerate(sorted_bunjang, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")

    def on_closing(self):
        # 크롤러 종료
        self.crawler_bunjang.close()
        self.crawler_joongonara.close()
        self.master.destroy()
