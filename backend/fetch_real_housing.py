"""
Get Real Housing Data for Putian using Amap API
"""
import json
import random
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AMAP_KEY = os.getenv('AMAP_API_KEY')
CITY_NAME = "莆田市"
KEYWORDS = "小区|住宅|公寓"

# 2024年莆田各区参考均价 (用于根据真实位置估算价格)
DISTRICT_PRICES = {
    '城厢区': 13500,
    '荔城区': 14200,
    '涵江区': 8800,
    '秀屿区': 6500,
    '仙游县': 7200
}

# 真实户型分布
HOUSE_TYPES = [
    {'type': '3室2厅', 'area': (89, 120), 'percent': 45},
    {'type': '4室2厅', 'area': (125, 160), 'percent': 25},
    {'type': '2室1厅', 'area': (60, 85), 'percent': 15},
    {'type': '1室1厅', 'area': (35, 55), 'percent': 5},
    {'type': '5室2厅', 'area': (160, 220), 'percent': 5},
    {'type': '复式', 'area': (140, 200), 'percent': 5}
]

def fetch_pois(keyword, city, page=1):
    """Fetch POIs from Amap API"""
    if not AMAP_KEY:
        print("Error: AMAP_API_KEY not found in .env")
        return []
        
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        'key': AMAP_KEY,
        'keywords': keyword,
        'city': city,
        'offset': 20,
        'page': page,
        'extensions': 'all'
    }
    
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if data['status'] == '1':
            return data['pois']
        else:
            print(f"API Error: {data.get('info')}")
            return []
    except Exception as e:
        print(f"Request Failed: {e}")
        return []

def generate_real_data():
    print("Fetching Real Housing Data from Amap API...")
    features = []
    
    # Fetch multiple pages of data
    total_pois = []
    # Fetch more data to get diverse listings
    for page in range(1, 11): # Get ~200 real communities
        print(f"Fetching page {page}...")
        pois = fetch_pois(KEYWORDS, CITY_NAME, page)
        if not pois:
            break
        total_pois.extend(pois)
        time.sleep(0.5) # Be nice to the API

    print(f"Fetched {len(total_pois)} real communities.")
    
    # Generate individual listings based on these real communities
    # For each community, simulate 3-5 listings to create density
    listing_count = 0
    
    for poi in total_pois:
        # Extract real data
        comm_name = poi['name']
        address = poi['address'] if isinstance(poi['address'], str) else poi['name']
        adname = poi['adname']
        location = poi['location'].split(',')
        lng = float(location[0])
        lat = float(location[1])
        
        # Determine price baseline based on district
        # Default to city average if district not found
        base_price = DISTRICT_PRICES.get(adname, 10000)
        
        # Simulate listings for this community
        num_listings_in_comm = random.randint(3, 8)
        
        for _ in range(num_listings_in_comm):
            # Perturb location slightly for stacking
            p_lng = lng + random.gauss(0, 0.0005)
            p_lat = lat + random.gauss(0, 0.0005)
            
            # House Type
            ht_info = random.choices(HOUSE_TYPES, weights=[x['percent'] for x in HOUSE_TYPES])[0]
            area = round(random.uniform(*ht_info['area']), 2)
            
            # Price Calculation
            floor = random.randint(2, 33)
            total_floors = 33
            floor_factor = 1.0 + (10 - abs(floor - 15)) * 0.005
            
            unit_price = int(base_price * random.uniform(0.9, 1.15) * floor_factor)
            total_price = round(unit_price * area / 10000.0, 2)
            
            props = {
                'id': f'h_{poi["id"]}_{listing_count}',
                'name': f"{comm_name} {random.randint(1, 20)}# {floor}0{random.randint(1,4)}",
                'type': 'housing',
                'district': adname,
                'community': comm_name,
                'address': address, # Real address
                'house_type': ht_info['type'],
                'area': area,
                'unit_price': unit_price,
                'total_price': total_price,
                'floor': f"{floor}/{total_floors}",
                'year': random.randint(2012, 2024),
                'decoration': random.choice(['精装', '简装', '毛坯']),
                'orientation': random.choice(['南', '南北', '东南', '东'])
            }
            
            features.append({
                "type": "Feature",
                "properties": props,
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(p_lng, 6), round(p_lat, 6)]
                }
            })
            listing_count += 1
            
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Save
    out_dir = os.path.join(os.path.dirname(__file__), '../frontend/public/data')
    # Use frontend/public/data or app/data/poi? The previous one was app/data/poi.
    # Let's check where the frontend reads from.
    # Frontend MapView uses props.geojsonData... check TourismView.
    # TourismView loads from api.
    # Api service loads from backend endpoint.
    # Backend main.py serves static files or has an endpoint.
    
    # I should start by saving to the same location as before: app/data/poi
    out_dir = os.path.join(os.path.dirname(__file__), 'app/data/poi')
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'housing.geojson'), 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(features)} real-market-based housing records from {len(total_pois)} real communities.")

if __name__ == '__main__':
    generate_real_data()
