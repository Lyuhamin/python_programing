from flask import Flask, jsonify, request, render_template
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler
import threading
import tkinter as tk
from gui import SearchApp  # SearchApp 임포트

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    
    # 최소 가격 및 최대 가격을 안전하게 처리
    min_price = request.form.get('min_price', '0')
    max_price = request.form.get('max_price', '')
    min_price = int(min_price) if min_price.isdigit() else 0
    max_price = int(max_price) if max_price.isdigit() else float('inf')

    bunjang_crawler = BunjangCrawler()
    joongonara_crawler = JoongonaraCrawler()

    results_bunjang = bunjang_crawler.crawl(keyword)
    results_joongonara = joongonara_crawler.crawl(keyword)

    # 가격 필터 적용
    filtered_results_bunjang = [item for item in results_bunjang if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_joongonara = [item for item in results_joongonara if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]

    bunjang_crawler.close()
    joongonara_crawler.close()

    # Tkinter 창 실행
    threading.Thread(target=run_tkinter, args=(keyword, filtered_results_bunjang, filtered_results_joongonara)).start()

    return jsonify({
        "keyword": keyword,
        "min_price": min_price,
        "max_price": max_price,
        "results_bunjang": filtered_results_bunjang,
        "results_joongonara": filtered_results_joongonara
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
