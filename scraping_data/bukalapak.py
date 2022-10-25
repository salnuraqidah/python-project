import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

url = 'https://www.bukalapak.com/products?'


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

params = {
   'search[keywords]': 'macbook air m1',
   'search[sort_by]':'weekly_sales_ratio:desc',
   'page':1
}

def get_total_pages(searches):
    params['search[keywords]']= searches
    res = requests.get(url, headers=headers, params=params)

    soup = BeautifulSoup(res.content, 'html.parser')
    
    pages = []

    headers_contents = soup.find('ul','bl-pagination__list').find_all('li')

    for i in headers_contents:
        try:
            pages.append(int(i.text))
        except:
            continue
    total_pages = max(pages)
    return total_pages

def output(searches, final_result):
    df = pd.DataFrame(final_result)
    # df.to_csv(f'{searches}.csv',index=False)
    df.to_excel(f'{searches}.xlsx')
    
    
def get_all_item(searches, pages):
    data = []
    params['search[keywords]']= searches
    params['page']= pages

    res = requests.get(url, headers=headers, params=params)

    soup = BeautifulSoup(res.content, 'html.parser')
    contents = soup.find_all('div','bl-flex-item mb-8')
    

    for content in contents:
        try:
            title = content.find('p','bl-text bl-text--body-14 bl-text--ellipsis__2').text.strip()
        except:
            title = ''
        
        try:
            link = content.find('a','bl-link')['href']
        except:
            link = ''
        
        try:
            price = content.find('p','bl-text bl-text--subheading-20 bl-text--semi-bold bl-text--ellipsis__1').text.strip().strip('Rp')
        except:
            price = ''
        
        try:
            rating = content.find('p','bl-text bl-text--body-14 bl-text--subdued').text.strip()
        except:
            rating = ''
        
        try:
            loc = content.find('span','mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1').text
        except:
            loc = ''
        
        try:
            store = content.find('span','bl-product-card__store bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1').text
        except:
            store = ''
        
        try:
            link_store = content.find('span','bl-product-card__store bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1').find('a')['href']
        except:
            link_store = ''
        if (title == '' and price == '' and loc=='' and store=='' and rating=='' and link_store=='' and link==''):
            continue
        else:
            final_data = {
                'title' : title,
                'price' : price,
                'location' : loc,
                'store' : store,
                'rating' : rating,
                'link_store' : link_store,
                'link' : link,
            }
            data.append(final_data)
    return data

def main(searches):
    final_result = []
    total_pages = get_total_pages(searches)
    for page in range(total_pages):
        page += 1
        print(f'Scraping halaman ke:{page}')
        products = get_all_item(searches,page)
        final_result += products
    
    total_data = len(final_result)
    print('Ini adalah halaman yang sudah discraping jumlah: '+ str(total_data))
    
    output(searches, final_result)

if __name__ == '__main__':
    searches = ('macbook air m1')
    main(searches)
    

