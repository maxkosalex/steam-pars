#steam-pars 2.2

import random
import sqlite3
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
s = Service(executable_path="/path/chromedriver")

driver = webdriver.Chrome(service=s, options=options)

item_href = None

# База данных

db = sqlite3.connect('steam-pars.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS steam_items (
    item_name text,
    coast_buy REAL,
    count_buy integer,
    coast_sell REAL,
    count_sell integer,
    item_link text
)""")

###

n = 1
all_pages = 2

def buy():
    try:
        buy_items = driver.find_element(By.ID, "market_commodity_forsale_table")
        buy_price = buy_items.find_elements(By.CSS_SELECTOR, "tr > td")  # .get_attribute('innerHTML')
    
        buy_prices = []
        buy_counts = 0
    
        print("buy")
        for k in range(len(buy_price)):
            if k % 2 == 0:
                buy_prices += re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', buy_price[k].text)
    
                print(k, "Цена " + " ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', buy_price[k].text)))  # get_attribute('innerHTML'))
            else:
                buy_counts += int(" ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', buy_price[k].text)))
    
                print(k, "Кол-во " + " ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', buy_price[k].text)))  # get_attribute('innerHTML'))
    
        if len(buy_prices) > 1:
            buy_price_one = buy_prices[1]
        else:
            buy_price_one = buy_prices[0]
    
        ###
    
        cursor.execute("UPDATE steam_items SET coast_buy = ?, count_buy = ?  WHERE item_link = ?", (buy_price_one, buy_counts, item_href))
        db.commit()
    
        ###
    
        time.sleep(random.randint(1, 3))
        
    except Exception as ex:
        print(ex):


def sell():
    try:
        sell_items = driver.find_element(By.ID, "market_commodity_buyreqeusts_table")
        sell_price = sell_items.find_elements(By.CSS_SELECTOR, "tr > td")
        print("sell")
    
        sell_prices = []
        sell_counts = 0
    
        for k in range(len(sell_price)):
            if k % 2 == 0:
                sell_prices += re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', sell_price[k].text)
    
                print(k, "Цена " + " ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', sell_price[k].text)))  # get_attribute('innerHTML'))
            else:
                sell_counts += int(" ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', sell_price[k].text)))
    
                print(k, "Кол-во " + " ".join(
                    re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', sell_price[k].text)))  # get_attribute('innerHTML'))
    
        sell_price_one = sell_prices[0]
    
        ###
    
        cursor.execute("UPDATE steam_items SET coast_sell = ?, count_sell = ?  WHERE item_link = ?", (sell_price_one, sell_counts, item_href))
        db.commit()
        
        ###
    
        time.sleep(random.randint(1, 3))
        
    except Exception as ex:
        print(ex):


while n < all_pages:
    try:
    
        driver.get("https://steamcommunity.com/market/search?q=#p1")

        time.sleep(1)
        all_pages = int(driver.find_elements(By.CLASS_NAME, "market_paging_pagelink")[-1].text)
    
        shop_list = driver.find_element(By.ID, "searchResultsRows")
        all_positions = shop_list.find_elements(By.CLASS_NAME, "market_listing_row_link")
        all_positions_href = [href.get_attribute('href') for href in all_positions]
    
        time.sleep(3)
        for i in range(len(all_positions_href)):
            time.sleep(random.randint(3, 6))
            driver.get(all_positions_href[i])
    
            item_href = all_positions_href[i]
    
            item_name = driver.find_element(By.CLASS_NAME, "hover_item_name").text
    
            cursor.execute("SELECT item_link FROM steam_items WHERE item_link = ?", (item_href,))

            print(n, item_name, item_href)

            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO steam_items (item_name, item_link) VALUES (?, ?)", (item_name, item_href))
            else:
                print('Такой предмет есть')
    
            time.sleep(5)  # важно не убирать

            buy()
            sell()
    n += 1
    
        # print(all_positions_href, "/h", buy_price)
    
    except Exception as ex:
        print(ex)

driver.close()
driver.quit()
db.close()
