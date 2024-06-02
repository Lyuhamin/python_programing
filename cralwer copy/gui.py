# gui.py

import tkinter as tk
from tkinter import ttk

class SearchApp:
    def __init__(self, master, keyword, results_bunjang, results_joongonara):
        self.master = master
        master.title("중고거래 도우미")
        master.geometry("400x600")  # 창 크기 설정

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label = ttk.Label(self.frame, text=f"검색어: {keyword}")
        self.label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(self.frame, height=30, width=50)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if results_joongonara:
            for idx, (title, price, link) in enumerate(results_joongonara, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")
        
        self.result_text.insert(tk.END, "\n번개장터 결과:\n")
        if results_bunjang:
            for idx, (title, price, link) in enumerate(results_bunjang, start=1):
                self.result_text.insert(tk.END, f"{idx}. 제목: {title}\n   가격: {price}\n   링크: {link}\n\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()
