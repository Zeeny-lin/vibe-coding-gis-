# -*- coding: utf-8 -*-
"""检查POI坐标是否在莆田范围内"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

poi_dir = 'app/data/poi'
invalid = []

# 莆田市范围: 经度118.5-119.5, 纬度24.8-25.8
MIN_LNG, MAX_LNG = 118.5, 119.5
MIN_LAT, MAX_LAT = 24.8, 25.8

for f in os.listdir(poi_dir):
    if f.endswith('.geojson'):
        with open(os.path.join(poi_dir, f), 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            for feat in data.get('features', []):
                geom = feat.get('geometry', {})
                coords = geom.get('coordinates', [])
                geom_type = geom.get('type', 'Point')
                
                # 跳过线要素
                if geom_type != 'Point':
                    continue
                    
                if len(coords) >= 2:
                    lng, lat = coords[0], coords[1]
                    # 检查是否在范围内
                    if not (MIN_LNG <= lng <= MAX_LNG and MIN_LAT <= lat <= MAX_LAT):
                        name = feat.get('properties', {}).get('name', 'unknown')
                        invalid.append({
                            'file': f,
                            'name': name,
                            'coords': [lng, lat]
                        })

print(f'发现 {len(invalid)} 个坐标异常的POI点:')
for i in invalid[:20]:
    print(f"  {i['file']}: {i['name']} -> {i['coords']}")
if len(invalid) > 20:
    print(f'  ... 还有 {len(invalid)-20} 个')
