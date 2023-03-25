#steampars
from bs4 import BeautifulSoup
from random import randint

import time
import re
import requests
import csv

with open("steam_data.csv", "w+") as file:
    writer = csv.writer(file)
    writer.writerow(
    ("Название", "Стоимость Покупки", "Стоимость Продажи", "Прибыль" , "Процент", "ссылка")
    )
def record_data():
    with open("steam_data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerows(zip(*all_data))
        
cookies = {
    "Your cookies",
}

headers = {
    "Your headers",
}

#Начальные переменные
start = 2500
count = 10
total_count = start + count
steam_procent = 0.13
names, coasts, sales, profits, procents, hrefs, all_data = [ ], [ ], [ ], [ ], [ ], [ ], [ ]

while start < total_count: #Главное тело цикла
    params = {
        'query': '',
        'start': str(start), #Место с какого кол-во предметов начинается поиск предметов
        'count': str(count), # Кол-во предметов на странице
        'search_descriptions': '0',
        'sort_column': 'price',
        'sort_dir': 'asc',
        'appid': '730',
        'category_730_ItemSet[]': 'any',
        'category_730_ProPlayer[]': 'any',
        'category_730_StickerCapsule[]': 'any',
        'category_730_TournamentTeam[]': 'any',
        'category_730_Weapon[]': 'any',
        'category_730_Quality[]': 'tag_normal',
        'category_730_Type[]': [
            'tag_CSGO_Type_Pistol',
            'tag_CSGO_Type_SMG',
            'tag_CSGO_Type_Rifle',
            'tag_CSGO_Type_Shotgun',
            'tag_CSGO_Type_SniperRifle',
            'tag_CSGO_Type_Machinegun',
        ],
    }
    
    response = requests.get('https://steamcommunity.com/market/search/render/', params=params, cookies=cookies, headers=headers) #Запрос главной ТП steam
        
    json=response.json()
    
    total_count=json["total_count"] #Общее число предметов
    json_soup = BeautifulSoup(json["results_html"], "lxml")

    data = json_soup.find_all("a", {"class":"market_listing_row_link"})
    
    for i in data: #Поиск каждого элемента
        
        name=i.find("div", {"class":"market_listing_row"}).get("data-hash-name")
        names.append(name)
        
        href = i.get("href")
        hrefs.append(href)
    
        response_item = requests.get(href, headers=headers, cookies=cookies) #Запрос на страницу кокретного премдета
        try:
            item_nameid = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(response_item.content))[0] #Находит айди предмета
            print(item_nameid)
            
            params_item = {
            'item_nameid': str(item_nameid),
            'language': 'russian',
            'currency': '1',    
            }
        
            item_response = requests.get('https://steamcommunity.com/market/itemordershistogram', params=params_item, headers = headers) #Запрос xhr файла
            
            """if item_response.status_code != 200:
                all_data.extend((names, sales, coasts, profits, procents, hrefs))
                print(all_data)
                record_data()"""        
            
            item_json = item_response.json()
            
            highest_buy_order = (int(item_json["highest_buy_order"])/100)
            sales.append("$"+str(highest_buy_order))
                    
            lowest_sell_order = (int(item_json["lowest_sell_order"])/100)
            coasts.append("$"+str(lowest_sell_order))
            
            profit = "$"+str(round(((lowest_sell_order - (lowest_sell_order*steam_procent))-highest_buy_order), 4)) #Расчет предполагаемой прибыли
            profits.append(profit)
                    
            procent = str(round(((lowest_sell_order - (lowest_sell_order*steam_procent))/highest_buy_order-1)*100, 4))+"%" #Расчет процента прибыли
            procents.append(procent)
            
        except Exception:
            print("Error" , item_response.status_code)
        
        #print(name, highest_buy_order, lowest_sell_order, profit, procent, href)
        
        time.sleep(366) #Время задержки следующего запроса
        
    all_data.extend((names, sales, coasts, profits, procents, hrefs))
    print("Successful!",all_data)
    
    start+=count
    
    record_data()
