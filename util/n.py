from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path= r'C:\\Utility\\BrowserDrivers\\chromedriver.exe')

driver.get("https://shopee.com.my/shop/13377506/search?page=0&sortBy=sales")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shop-search-result-view')))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
search = soup.select_one('.shop-search-result-view')
products = search.find_all('a')

for p in products:
    name = p.select('div[data-sqe="name"] > div')[0].get_text()
    price = p.select('div > div:nth-child(2) > div:nth-child(2)')[0].get_text()
    product = p.select('div > div:nth-child(2) > div:nth-child(4)')[0].get_text()
    print('name: ' + name)
    print('price: ' + price)
    print('product: ' + product + '\n')