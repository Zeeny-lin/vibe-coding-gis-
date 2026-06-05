
import os
import requests
from dotenv import load_dotenv

load_dotenv()

AMAP_KEY = os.getenv('AMAP_API_KEY')
CITY = "莆田市"
SPOTS = [
    "湄洲妈祖祖庙",
    "天妃故里",
    "妈祖文化园",
    "湄洲岛黄金沙滩",
    "妈祖影视城",
    "九鲤湖",
    "广化寺",
    "南少林寺"
]

def fetch_coords(keyword):
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        'key': AMAP_KEY,
        'keywords': keyword,
        'city': CITY,
        'extensions': 'all'
    }
    
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if data['status'] == '1' and len(data['pois']) > 0:
            location = data['pois'][0]['location'] # "lng,lat"
            lng, lat = map(float, location.split(','))
            return [lng, lat]
    except Exception as e:
        print(f"Error fetching {keyword}: {e}")
    return None

def main():
    if not AMAP_KEY:
        print("Error: AMAP_API_KEY not found.")
        return

    results = {}
    print("Fetching coordinates...")
    for spot in SPOTS:
        coords = fetch_coords(spot)
        if coords:
            print(f"{spot}: {coords}")
            results[spot] = coords
        else:
            print(f"{spot}: Not Found")
    
    print("\n\nReady to copy-paste dictionary:")
    print(results)

if __name__ == "__main__":
    main()
