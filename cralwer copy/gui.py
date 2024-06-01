# gui.py

import tkinter as tk
from tkinter import ttk
import requests

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

        self.result_text = tk.Text(self.frame, height=20, width=60)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search(self):
        keyword = self.entry.get()
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 중...\n")

        response = requests.post('http://127.0.0.1:5000/search', data={'keyword': keyword})
        data = response.json()

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"검색어: {data['keyword']}\n\n")
        
        self.result_text.insert(tk.END, "중고나라 결과:\n")
        if data['results_joongonara']:
            for title, price in data['results_joongonara']:
                self.result_text.insert(tk.END, f"{title} - {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")
        
        self.result_text.insert(tk.END, "\n번개장터 결과:\n")
        if data['results_bunjang']:
            for title, price in data['results_bunjang']:
                self.result_text.insert(tk.END, f"{title} - {price}\n")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.\n")

    def on_closing(self):
        self.master.destroy()
