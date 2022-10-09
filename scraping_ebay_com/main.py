import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

url = 'https://www.ebay.com/sch/i.html?'
base_url = 'https://www.ebay.com/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
result = []

def get_total_pages(searches):    
    params = {
        '_from': 'R40',
        '_trksid': 'p2380057.m570.l1313',
        '_sacat': '0',
        '_pgn' : 1,
        '_nkw' : searches
    }

    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    pages = []

    headers_contents = soup.find('nav','pagination').find_all('a')
    
    for i in headers_contents:
        try:
            pages.append(int(i.text))
        except:
            continue
    total_pages = max(pages)
    return total_pages

def get_all_item(searches, pages):
    iphonelist = []
    
    params = {
        '_from': 'R40',
        '_trksid': 'p2380057.m570.l1313',
        '_sacat': '0',
        '_pgn' : pages,
        '_nkw' : searches
    }
    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    results = soup.find('div',{'class':'srp-river-results clearfix'})
    contents = soup.find_all('li','s-item s-item__pl-on-bottom')

    for content in contents:
        title = content.find('div','s-item__title').text
        try:
            price = content.find('span','s-item__price').text
        except:
            continue
        
        try:
            location = content.find('span','s-item__itemLocation').text.strip().split('from ')[1]
        except:
            continue
        
        try:
            review = content.find('span','s-item__reviews-count').text
        except:
            review = 'no review'
        
        final_data = {
            'title' : title,
            'price' : price,
            'location' : location,
            'review' : review,
        }
        iphonelist.append(final_data)
    return iphonelist
    
def output(searches, final_result):
    df = pd.DataFrame(final_result)
    df.to_csv(f'{searches}.csv',index=False)

def main(searches):
    final_result = []
    total_pages = get_total_pages(searches)
    for page in range(total_pages):
        page += 1
        print(f'Scraping halaman ke:{page}')
        products = get_all_item(searches,page)
        final_result += products
    
    total_data = len(final_result)
    print('Ini adalah halaman yang sudah discraping'. format(total_data))
    
    output(searches, final_result)

if __name__ == '__main__':
    searches = ('iphone')
    main(searches)

    