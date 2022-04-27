from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv

# create object for chrome options
chrome_options = Options()
base_url = 'https://shopee.com.my/shop/13377506/search?page=0&sortBy=sales'

# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('user-data-dir=C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })
# invoke the webdriver
browser = webdriver.Chrome(executable_path = r'C:/Users/username/Documents/playground_python/chromedriver.exe',
                          options = chrome_options)
browser.get(base_url)
delay = 5 #secods

# declare empty lists
item_cost, item_init_cost, item_loc = [],[],[]
item_name, items_sold, discount_percent = [], [], []
while True:
    try:
        WebDriverWait(browser, delay)
        print ("Page is ready")
        sleep(5)
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        #print(html)
        soup = BeautifulSoup(html, "html.parser")

        # find_all() returns an array of elements. 
        # We have to go through all of them and select that one you are need. And than call get_text()
        for item_n in soup.find_all('div', class_='_1NoI8_ _16BAGk'):
            print(item_n.get_text())
            item_name.append(item_n.text)

        # find the price of items
        for item_c in soup.find_all('span', class_='_341bF0'):
            print(item_c.get_text())
            item_cost.append(item_c.text)

        # find initial item cost
        for item_ic in soup.find_all('div', class_ = '_1w9jLI QbH7Ig U90Nhh'):
            print(item_ic.get_text())
            item_init_cost.append(item_ic.text)
        # find total number of items sold/month
        for items_s in soup.find_all('div',class_ = '_18SLBt'):
            print(items_s.get_text())
            items_sold.append(item_ic.text)

        # find item discount percent
        for dp in soup.find_all('span', class_ = 'percent'):
            print(dp.get_text())
            discount_percent.append(dp.text)
        # find item location
        for il in soup.find_all('div', class_ = '_3amru2'):
            print(il.get_text())
            item_loc.append(il.text)

        break # it will break from the loop once the specific element will be present. 
    except TimeoutException:
        print ("Loading took too much time!-Try again")

rows = zip(item_name, item_init_cost,discount_percent,item_cost,items_sold,item_loc)
newFilePath = 'shopee_item_list.csv'
with open(newFilePath, "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
