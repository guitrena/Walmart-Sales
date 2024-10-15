from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.use_chromium = True
options.add_argument("--headless") 
options.add_argument("--disable-gpu") 
options.add_argument("--start-maximized")

service = Service(r'C:\Users\Guillermo\python\edgedriver_win64\msedgedriver.exe')

driver = webdriver.Edge(service=service, options=options)

driver.get("http://localhost:56648/")

time.sleep(10)

page_height = driver.execute_script("return document.body.scrollHeight")

driver.set_window_size(1520, page_height+170)

driver.save_screenshot("./Images/dashboard_example22.png")

time.sleep(10)

driver.quit()
