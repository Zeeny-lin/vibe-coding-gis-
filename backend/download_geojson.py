import requests
import json
import os

url = "https://geo.datav.aliyun.com/areas_v3/bound/350300_full.json"
output_path = r"c:\Users\liuhao\Desktop\GIS程序设计\putian-gis\backend\app\data\districts.geojson"

try:
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")
