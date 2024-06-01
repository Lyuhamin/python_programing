# server.py

from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    product = request.form['product']
    results = perform_search(product)
    return jsonify(results)

def perform_search(keyword):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://google.com")

    search_bar = browser.find_element(By.NAME, "q")
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "g"))
    )

    search_results = browser.find_elements(By.CLASS_NAME, "g")[:10]  # 첫 10개 결과만 가져옴

    results = []
    for search_result in search_results:
        try:
            title = search_result.find_element(By.TAG_NAME, "h3").text
            link = search_result.find_element(By.TAG_NAME, "a").get_attribute("href")
            results.append({"title": title, "link": link})
        except:
            continue

    browser.quit()
    return results

if __name__ == '__main__':
    app.run(debug=True)
