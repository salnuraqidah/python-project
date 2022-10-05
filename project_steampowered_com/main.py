import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://store.steampowered.com/search/?term=gta'

def get_data(url):
    r = requests.get(url)
    return r.text

#pocessing data
def parse(data):
    result = []
    soup = BeautifulSoup(data, 'html.parser')
    contents = soup.find('div',attrs={'id':'search_resultsRows'})
    games = contents.find_all('a')
    
    for game in games:
        link = game['href']
    
        # parsing data
        title = game.find('span',{'class' : 'title'}).text
        price = game.find('div',{'class':'search_price'}).text.strip('E')

        # sorting data 
        data_dict = {
            'title' : title,
            'price' : price,
            'link' : link
        }

        # append 
        result.append(data_dict)
    return result

# process cleaned data from parser 

def output (datas: list):
    for i in datas:
        print(i)

if __name__ == '__main__':
    data = get_data(url)

    final_data = parse(data)
    output(final_data)