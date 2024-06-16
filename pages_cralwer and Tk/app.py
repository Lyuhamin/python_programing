import threading
from flask import Flask, render_template, request, jsonify
from hellomarket_crawler import HellomarketCrawler
from joongonara_crawler import JoongonaraCrawler
from fruitfamily_crawler import FruitfamilyCrawler
from yes24_crawler import Yes24Crawler  # Yes24 크롤러 추가
from aladin_crawler import AladinCrawler  # Aladin 크롤러 추가
from tkinter import Tk, Label, Entry, Button, END

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    min_price = request.form.get('min_price', '0')
    max_price = request.form.get('max_price', '')
    min_price = int(min_price) if min_price.isdigit() else 0
    max_price = int(max_price) if max_price.isdigit() else 1_000_000_000  # 무한대 대신 큰 값 사용

    hellomarket_crawler = HellomarketCrawler()
    joongonara_crawler = JoongonaraCrawler()
    fruitfamily_crawler = FruitfamilyCrawler()
    yes24_crawler = Yes24Crawler()  # Yes24 크롤러 추가
    aladin_crawler = AladinCrawler()  # Aladin 크롤러 추가

    results_hellomarket = hellomarket_crawler.crawl(keyword)
    results_joongonara = joongonara_crawler.crawl(keyword)
    results_fruitfamily = fruitfamily_crawler.crawl(keyword)
    results_yes24 = yes24_crawler.crawl(keyword)  # Yes24 크롤러 결과 추가
    results_aladin = aladin_crawler.crawl(keyword)  # Aladin 크롤러 결과 추가

    hellomarket_crawler.close()
    joongonara_crawler.close()
    fruitfamily_crawler.close()
    yes24_crawler.close()
    aladin_crawler.close()

    filtered_results_hellomarket = [item for item in results_hellomarket if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_joongonara = [item for item in results_joongonara if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_fruitfamily = [item for item in results_fruitfamily if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_yes24 = [item for item in results_yes24 if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_aladin = [item for item in results_aladin if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]

    return render_template('results.html', 
                           keyword=keyword, 
                           results_hellomarket=filtered_results_hellomarket, 
                           results_joongonara=filtered_results_joongonara,
                           results_fruitfamily=filtered_results_fruitfamily,
                           results_yes24=filtered_results_yes24,  # Yes24 결과 전달
                           results_aladin=filtered_results_aladin)  # Aladin 결과 전달

@app.route('/search_sorted', methods=['POST'])
def search_sorted():
    sort_type = request.json.get('sort', 'price_asc')

    keyword = request.json.get('keyword', '')
    min_price = int(request.json.get('min_price', 0))
    max_price = request.json.get('max_price', 1_000_000_000)  # 무한대 대신 큰 값 사용

    hellomarket_crawler = HellomarketCrawler()
    joongonara_crawler = JoongonaraCrawler()
    fruitfamily_crawler = FruitfamilyCrawler()
    yes24_crawler = Yes24Crawler()  # Yes24 크롤러 추가
    aladin_crawler = AladinCrawler()  # Aladin 크롤러 추가

    results_hellomarket = hellomarket_crawler.crawl(keyword)
    results_joongonara = joongonara_crawler.crawl(keyword)
    results_fruitfamily = fruitfamily_crawler.crawl(keyword)
    results_yes24 = yes24_crawler.crawl(keyword)  # Yes24 크롤러 결과 추가
    results_aladin = aladin_crawler.crawl(keyword)  # Aladin 크롤러 결과 추가

    hellomarket_crawler.close()
    joongonara_crawler.close()
    fruitfamily_crawler.close()
    yes24_crawler.close()
    aladin_crawler.close()

    filtered_results_hellomarket = [item for item in results_hellomarket if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_joongonara = [item for item in results_joongonara if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_fruitfamily = [item for item in results_fruitfamily if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_yes24 = [item for item in results_yes24 if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_aladin = [item for item in results_aladin if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]

    if sort_type == 'price_asc':
        filtered_results_hellomarket.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))
        filtered_results_joongonara.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))
        filtered_results_fruitfamily.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))
        filtered_results_yes24.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))
        filtered_results_aladin.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))

    return jsonify({
        'results_hellomarket': filtered_results_hellomarket,
        'results_joongonara': filtered_results_joongonara,
        'results_fruitfamily': filtered_results_fruitfamily,
        'results_yes24': filtered_results_yes24,  # Yes24 결과 추가
        'results_aladin': filtered_results_aladin  # Aladin 결과 추가
    })

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask()
