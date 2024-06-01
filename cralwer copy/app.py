# app.py

from flask import Flask, render_template, request
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler
import threading

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

    return render_template('results.html', keyword=keyword, results_bunjang=results_bunjang, results_joongonara=results_joongonara)

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
