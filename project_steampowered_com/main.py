import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


url = 'https://store.steampowered.com/search/?term=gta'

def get_data(url):
    r = requests.get(url)
    return r.text

#pocessing data
def parse(data):
    result = []
    soup = BeautifulSoup(data, 'html.parser')
    try:
      os.mkdir('json_result')
    except FileExistsError:
        pass
    contents = soup.find('div',attrs={'id':'search_resultsRows'})
    games = contents.find_all('a')
    
    for game in games:
        link = game['href']
    
        # parsing data
        title = game.find('span',{'class' : 'title'}).text.strip().split('£')[0]
        price = game.find('div',{'class':'search_price'}).text.strip().split('£')[0]
        release = game.find('div',{'class':'search_released'}).text.strip().split('£')[0]

        if release == '':
            release='none'

        # sorting data 
        data_dict = {
            'title' : title,
            'release' : release,
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

def generate_data(result, filename):
    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx',index=False)


if __name__ == '__main__':
    data = get_data(url)

    final_data = parse(data)
    namafile = input('Masukkan nama file:')
    generate_data(final_data,namafile)
    output(final_data)