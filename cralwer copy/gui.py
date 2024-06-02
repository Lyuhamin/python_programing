import tkinter as tk
from tkinter import ttk, scrolledtext

class SearchApp:
    def __init__(self, master, keyword, results_bunjang, results_joongonara):
        self.master = master
        master.title("중고거래 도우미")
        master.geometry("800x600")  # 창 크기를 더 크게 조정

        # 레이아웃 구성을 위한 프레임
        self.frame = ttk.Frame(master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)  # 프레임을 창에 꽉 채우도록 설정

        # 검색어 표시 레이블
        self.label = ttk.Label(self.frame, text=f"검색어: {keyword}", font=('Arial', 16))
        self.label.pack(fill=tk.X)  # 레이블을 위쪽에 고정

        # 스크롤 가능한 텍스트 상자
        self.result_text = scrolledtext.ScrolledText(self.frame, height=40, width=70, wrap=tk.WORD, font=('Arial', 12))
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=10)  # 텍스트 상자를 프레임에 꽉 채우도록 설정

        # 결과 표시
        self.display_results(results_bunjang, results_joongonara)

    def display_results(self, results_bunjang, results_joongonara):
        self.result_text.delete('1.0', tk.END)
        
        # 중고나라 결과 정렬 및 출력
        sorted_joongonara = sorted(results_joongonara, key=lambda x: int(x[1].replace(',', '').replace('원', '')))
        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if sorted_joongonara:
            for idx, (title, price, link) in enumerate(sorted_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

        # 번개장터 결과 정렬 및 출력
        sorted_bunjang = sorted(results_bunjang, key=lambda x: int(x[1].replace(',', '').replace('원', '')))
        self.result_text.insert(tk.END, "\n번개장터 결과:\n")
        if sorted_bunjang:
            for idx, (title, price, link) in enumerate(sorted_bunjang, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()
