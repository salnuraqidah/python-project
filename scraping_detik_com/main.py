import requests
from bs4 import BeautifulSoup

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

titles = contents.find_all('h2','title')
images = contents.find_all(attrs={'class':'ratiobox box_thumb'})

datas = contents.find_all('article')

for data in datas:
    print(data.find('h2','title').text)

