from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

KEYWORD = "중고"

browser = webdriver.Chrome()

browser.get("https://google.com")

search_bar = browser.find_element("name", "gLFyf")

search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)

shitty_element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "MjjYud"))
)

browser.execute_script(
    """
const shitty = arguments[0];
shitty.parentElement.removeChild(shitty)
""",
    shitty_element,
)

search_results = browser.find_element("name", "g")

for index, search_result in enumerate(search_results):
    search_result.screenshot(f"screenshots/{KEYWORD}x{index}.png")

browser.quit()