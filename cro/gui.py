import tkinter as tk
from tkinter import ttk
import csv
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler
import os

class SearchApp:
    def __init__(self, master):
        self.master = master
        self.joongonara_crawler = JoongonaraCrawler()
        self.bunjang_crawler = BunjangCrawler()
        
        master.title("중고거래 도우미")

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = ttk.Button(self.frame, text="검색", command=self.search)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.result_text = tk.Text(self.frame, height=20, width=60)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.load_button = ttk.Button(self.frame, text="저장 목록 보기", command=self.load_csv)
        self.load_button.grid(row=2, column=0, padx=5, pady=5)

    def search(self):
        keyword = self.entry.get()
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "검색 중...\n")

        self.master.after(100, self.update_results, keyword)

    def update_results(self, keyword):
        results_joongonara = self.joongonara_crawler.crawl(keyword)
        results_bunjang = self.bunjang_crawler.crawl(keyword)
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "중고나라 결과:\n")
        for title, price in results_joongonara:
            self.result_text.insert(tk.END, f"{title} - {price}\n")
        
        self.result_text.insert(tk.END, "\n번개장터 결과:\n")
        for title, price in results_bunjang:
            self.result_text.insert(tk.END, f"{title} - {price}\n")

        self.save_to_csv(keyword, results_joongonara, results_bunjang)

    def save_to_csv(self, keyword, results_joongonara, results_bunjang):
        filename = "results.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "Title", "Price"])
            for title, price in results_joongonara:
                writer.writerow(["Joongonara", title, price])
            for title, price in results_bunjang:
                writer.writerow(["Bunjang", title, price])
        
        self.result_text.insert(tk.END, f"\n결과가 파일에 저장되었습니다.\n")

    def load_csv(self):
        keyword = self.entry.get()
        filename = f"results.csv"
        if os.path.exists(filename):
            self.result_text.delete('1.0', tk.END)
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.result_text.insert(tk.END, ' - '.join(row) + '\n')
        else:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "CSV 파일이 존재하지 않습니다.\n")

    def on_closing(self):
        self.joongonara_crawler.close()
        self.bunjang_crawler.close()
        self.master.destroy()