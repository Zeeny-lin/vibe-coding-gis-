import requests
import json
import os

# 目标文件路径
output_path = r"app/data/districts.geojson"

# 阿里云GeoJSON地址 (莆田市)
url = "https://geo.datav.aliyun.com/areas_v3/bound/350300_full.json"

# 补充的统计数据 (模拟)
stats = {
    "城厢区": {"population": 46.8, "area": 509},
    "涵江区": {"population": 43.2, "area": 752},
    "荔城区": {"population": 56.8, "area": 269},
    "秀屿区": {"population": 56.5, "area": 842},
    "仙游县": {"population": 103.5, "area": 1835}
}

def update_geojson():
    try:
        print(f"正在下载数据: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # 处理每个Feature，添加统计属性
        for feature in data['features']:
            name = feature['properties']['name']
            if name in stats:
                feature['properties']['population'] = stats[name]['population']
                feature['properties']['area'] = stats[name]['area']
                feature['properties']['code'] = feature['properties']['adcode']
                # 确保中心点存在
                if 'centroid' in feature['properties']:
                     feature['properties']['center'] = feature['properties']['centroid']
                # 简化一些不需要的属性以减小体积
                keys_to_remove = ['childrenNum', 'level', 'parent', 'subFeatureIndex', 'acroutes']
                for key in keys_to_remove:
                    feature['properties'].pop(key, None)
                    
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"成功更新行政区划数据: {output_path}")
        
    except Exception as e:
        print(f"更新失败: {str(e)}")

if __name__ == "__main__":
    update_geojson()
