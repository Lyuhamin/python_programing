import threading
from flask import Flask, render_template, request
from bunjang_crawler import BunjangCrawler
from joonggonara_crawler import JoongonaraCrawler
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
    max_price = int(max_price) if max_price.isdigit() else float('inf')

    bunjang_crawler = BunjangCrawler()
    joongonara_crawler = JoongonaraCrawler()

    results_bunjang = bunjang_crawler.crawl(keyword)
    results_joongonara = joongonara_crawler.crawl(keyword)

    bunjang_crawler.close()
    joongonara_crawler.close()

    filtered_results_bunjang = [item for item in results_bunjang if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]
    filtered_results_joongonara = [item for item in results_joongonara if min_price <= int(item[1].replace(',', '').replace('원', '')) <= max_price]

    return render_template('results.html', 
                           keyword=keyword, 
                           results_bunjang=filtered_results_bunjang, 
                           results_joongonara=filtered_results_joongonara)

def run_flask():
    app.run(debug=True, use_reloader=False)

def run_tk():
    root = Tk()
    root.title("Search Interface")
    
    Label(root, text="Keyword:").grid(row=0, column=0)
    keyword_entry = Entry(root)
    keyword_entry.grid(row=0, column=1)
    
    Label(root, text="Min Price:").grid(row=1, column=0)
    min_price_entry = Entry(root)
    min_price_entry.grid(row=1, column=1)
    
    Label(root, text="Max Price:").grid(row=2, column=0)
    max_price_entry = Entry(root)
    max_price_entry.grid(row=2, column=1)
    
    def on_search():
        keyword = keyword_entry.get()
        min_price = min_price_entry.get()
        max_price = max_price_entry.get()
        request.form = {'keyword': keyword, 'min_price': min_price, 'max_price': max_price}
        search()  # Call the search function directly
    
    search_button = Button(root, text="Search", command=on_search)
    search_button.grid(row=3, column=0, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_tk()
