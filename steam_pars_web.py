#steam-pars 2.0

import random
import csv
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

all_data, all_buy_prices, all_buy_counts, all_sell_prices, all_sell_counts, all_profit, all_procent_profit, all_hrefs = [], 0, 0, 0, 0, [], [], []

origin_names = ("Название", "Стоимость Покупки", "Стоимость Продажи", "Прибыль", "Процент", "ссылка")

with open("steam_data.csv", "w+", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ("Название", "Стоимость Покупки", "кол-во", "Стоимость Продажи", "кол-во", "Прибыль", "Процент", "ссылка"))


def record_data():
    global all_data

    with open("steam_data.csv", "a") as file:
        writer = csv.writer(file)
        print(all_data)
        writer.writerows(all_data)


def buy():
    global all_buy_prices, all_buy_counts

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
        all_buy_prices = buy_prices[1]
    else:
        all_buy_prices = buy_prices[0]

    all_buy_counts = buy_counts

    time.sleep(random.randint(1, 3))


def sell():
    global all_sell_prices, all_sell_counts

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

    all_sell_prices = sell_prices[0]

    all_sell_counts = sell_counts

    time.sleep(random.randint(1, 3))


try:

    driver.get("https://steamcommunity.com/market/search?q=#p1")

    shop_list = driver.find_element(By.ID, "searchResultsRows")
    all_positions = shop_list.find_elements(By.CLASS_NAME, "market_listing_row_link")
    all_positions_href = [href.get_attribute('href') for href in all_positions]

    time.sleep(3)
    for i in range(len(all_positions_href)):
        time.sleep(random.randint(3, 6))
        driver.get(all_positions_href[i])

        all_hrefs.append(all_positions_href[i])

        item_name = driver.find_element(By.CLASS_NAME, "hover_item_name").text


        print(item_name)

        time.sleep(5)  # важно не убирать

        while True:
            try:

                buy()

                sell()

                break
            except Exception as ex:
                print(ex)


        all_data.append([item_name, all_buy_prices, all_buy_counts, all_sell_prices, all_sell_counts, all_profit,
                     all_procent_profit, all_positions_href[i]])



    # print(all_positions_href, "/h", buy_price)

except Exception as ex:
    driver.back()
    pass  # print(ex)
finally:
    driver.close()
    driver.quit()

record_data()
