from selenium.webdriver.chrome import options

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])