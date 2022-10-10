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
    
if __name__ == '__main__':
    app.run(debug=True)