import requests

url = 'http://www.floatrates.com/daily/idr.json'

json_data = requests.get(url).json()

for data in json_data.values():
    print(data['code'])
    print(data['name'])
    print(data['date'])
    print(data['inverseRate'])
    
    
    

