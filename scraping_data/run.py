import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('base.html',home=1)

@app.route("/logammulia")
def logammulia():
    url = 'https://www.detik.com/tag/logam-mulia?'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    params = {
    'tag_from': 'harga-emas'
    }

    res = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(res.content, 'html.parser')

    contents = soup.find('div','list media_rows list-berita')
    datas = contents.find_all('article')
    
    return render_template('detik_scraper.html', datas=datas)

@app.route('/idr-rates')
def idr_rates():
    url = 'http://www.floatrates.com/daily/idr.json'
    json_data = requests.get(url).json().values()
    return render_template('idr_rates.html', json_data=json_data)

@app.route('/bukalapak')
def bukalapak():
    url = 'https://www.bukalapak.com/products?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    params = {
        'search[keywords]': 'macbook air m1',
        'search[sort_by]':'weekly_sales_ratio:desc',
        'page':1
    }
    searches = 'macbook air m1'
    final_result = []
    total_pages = get_total_pages(searches,params,url,headers)
    for page in range(total_pages):
        page += 1
        products = get_all_item(searches,page,params,url,headers)
        final_result += products
    
    return render_template('bukalapak.html', datas=final_result)



def get_total_pages(searches,params,url,headers):
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
    
    
def get_all_item(searches, pages,params,url,headers):
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
            rating = content.find('p','bl-text bl-text--body-14 bl-text--subdued').text.strip().strip('Terjual')
        except:
            rating = '0'
        
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
        if (title == '' and price == '' and loc=='' and store=='' and rating=='0' and link_store=='' and link==''):
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
 
if __name__ == '__main__':
    app.run(debug=True)