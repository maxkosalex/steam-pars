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
    'timezoneOffset': '10800,0',
    '_ga': 'GA1.2.274522175.1679236447',
    '_gid': 'GA1.2.641940250.1679236447',
    'sessionid': '3b4f4133482d3bc79296552d',
    'steamCountry': 'RU%7C4fb27fd3eacde98e3f3e69fa5268bc49',
    'strResponsiveViewPrefs': 'touch',
}

headers = {
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'timezoneOffset=10800,0; _ga=GA1.2.274522175.1679236447; _gid=GA1.2.641940250.1679236447; sessionid=3b4f4133482d3bc79296552d; steamCountry=RU%7C4fb27fd3eacde98e3f3e69fa5268bc49; strResponsiveViewPrefs=touch',
    'Referer': 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Pistol&category_730_Type%5B%5D=tag_CSGO_Type_SMG&category_730_Type%5B%5D=tag_CSGO_Type_Rifle&category_730_Type%5B%5D=tag_CSGO_Type_Shotgun&category_730_Type%5B%5D=tag_CSGO_Type_SniperRifle&category_730_Type%5B%5D=tag_CSGO_Type_Machinegun&appid=730&q=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'X-Prototype-Version': '1.7',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

params = {
    'query': '',
    'start': '610',
    'count': '15',
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

response = requests.get('https://steamcommunity.com/market/search/render/', params=params, cookies=cookies, headers=headers)
    
all_json=response.json()

total_count=all_json["total_count"]
html=all_json["results_html"]
soup=BeautifulSoup(html, "lxml")
good_html=(str(soup).encode("ascii", "ignore").decode())

names, coasts, sales, profits, procents, hrefs, all_data = [ ], [ ], [ ], [ ], [ ], [ ], [ ]

steam_procent = 0.13

data = soup.find_all("a", {"class":"market_listing_row_link"})

for i in data:
    
    href = i.get("href")
    
    name=i.find("div", {"class":"market_listing_row"}).get("data-hash-name")

    response_item = requests.get(href, headers=headers, cookies=cookies)
    
    item_nameid = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(response_item.content))[0]
    
    params_item = {
    'item_nameid': str(item_nameid),
    'language': 'russian',
    'currency': '1',    
    }
    
    item_response = requests.get('https://steamcommunity.com/market/itemordershistogram', params=params_item, headers = headers, proxies=proxies)
    
    if item_response.status_code == 429:
        all_data.extend((names, sales, coasts, profits, procents, hrefs))
        print(all_data)
        record_data()
        
    print(item_response)
    item_json = item_response.json()
    highest_buy_order = (int(item_json["highest_buy_order"])/100)
    lowest_sell_order = (int(item_json["lowest_sell_order"])/100)
    
    profit = "$"+str(round(((lowest_sell_order - (lowest_sell_order*steam_procent))-highest_buy_order), 4))
    procent = str(round(((lowest_sell_order - (lowest_sell_order*steam_procent))/highest_buy_order-1)*100, 4))+"%"
    
    
    names.append(name)
    coasts.append("$"+str(lowest_sell_order))
    sales.append("$"+str(highest_buy_order))
    profits.append(profit)
    procents.append(procent)
    hrefs.append(href)
    
    
    print(name, highest_buy_order, lowest_sell_order, profit, procent, href)
    
    time.sleep(randint(5, 15))
    
all_data.extend((names, sales, coasts, profits, procents, hrefs))    
print(all_data)
record_data()   
