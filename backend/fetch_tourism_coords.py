import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

AMAP_KEY = os.getenv('AMAP_API_KEY')

def get_location(keyword, city="莆田市"):
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        'key': AMAP_KEY,
        'keywords': keyword,
        'city': city,
        'offset': 1,
        'page': 1,
        'extensions': 'all'
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if data['status'] == '1' and data['pois']:
            location = data['pois'][0]['location']
            lng, lat = map(float, location.split(','))
            return [lng, lat]
    except Exception as e:
        print(f"Error fetching {keyword}: {e}")
    return None

spots = [
    "湄洲妈祖祖庙", 
    "天妃故里", 
    "妈祖文化园", 
    "湄洲岛黄金沙滩", 
    "妈祖影视城", 
    "九鲤湖", 
    "广化寺", 
    "南少林寺"
]

results = {}
print("Fetching real coordinates...")
for spot in spots:
    coords = get_location(spot)
    if coords:
        print(f"{spot}: {coords}")
        results[spot] = coords
    else:
        print(f"{spot}: Not Found")
