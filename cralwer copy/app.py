from flask import Flask, jsonify, request, render_template
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler
import threading
import tkinter as tk
from tkinter import ttk
from gui import SearchApp  # SearchApp 임포트

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    bunjang_crawler = BunjangCrawler()
    joongonara_crawler = JoongonaraCrawler()

    results_bunjang = bunjang_crawler.crawl(keyword)
    results_joongonara = joongonara_crawler.crawl(keyword)

    bunjang_crawler.close()
    joongonara_crawler.close()

    # Tkinter 창 실행
    run_tkinter(keyword, results_bunjang, results_joongonara)

    return jsonify({
        "keyword": keyword,
        "results_bunjang": results_bunjang,
        "results_joongonara": results_joongonara
    })

def run_tkinter(keyword, results_bunjang, results_joongonara):
    root = tk.Tk()
    app = SearchApp(root, keyword, results_bunjang, results_joongonara)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
