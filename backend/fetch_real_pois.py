
import requests
import json
import os
import time
import urllib3

# 禁用安全请求警告（针对SSL验证问题）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 配置区 =================
# 高德地图Web服务API Key
AMAP_KEY = "f526ba6e95424e14f56d0f777cf82154"
# 莆田市区号
CITY_CODE = "0594" 
# POI搜索API地址
BASE_URL = "https://restapi.amap.com/v3/place/text"

# 想要获取的POI类型和关键词
# types参考高德POI分类编码表
POI_CONFIG = {
    "school": {
        "keywords": "中学|小学|职业技术学校|大学", 
        "types": "141200|141201|141202"
    },
    "hospital": {
        "keywords": "综合医院|专科医院", 
        "types": "090100|090101|090200"
    },
    "scenic": {
        "keywords": "风景名胜|公园|旅游景点", 
        "types": "110000|110200"
    },
    "mazu": {
        "keywords": "妈祖庙|天后宫|祖庙", 
        "types": "110205"
    }
}

# 输出目录
OUTPUT_DIR = r"app/data/poi"
# =========================================

def fetch_pois_from_amap(category, keywords, types):
    """
    从高德API获取指定类型的POI数据
    """
    all_pois = []
    page = 1
    max_pages = 5  # 每个分类最多获取5页(约100条)，防止数据过多
    
    print(f"正在获取 [{category}] 类数据 (关键词: {keywords})...")
    
    while page <= max_pages:
        try:
            params = {
                "key": AMAP_KEY,
                "keywords": keywords,
                "types": types,
                "city": CITY_CODE,
                "citylimit": "true",  # 限制在城市内
                "offset": 20,         # 每页20条
                "page": page,
                "extensions": "base"
            }
            
            # 发起请求
            # 注意：verify=False 是为了解决部分网络环境下SSL证书验证失败的问题
            # 如果你在好的网络环境下可以尝试去掉 verify=False
            response = requests.get(BASE_URL, params=params, verify=False, timeout=10)
            
            if response.status_code != 200:
                print(f"  请求失败，状态码: {response.status_code}")
                break
                
            data = response.json()
            
            if data["status"] == "1":
                pois = data.get("pois", [])
                if not pois:
                    print(f"  第 {page} 页无数据，结束获取。")
                    break
                
                print(f"  获取第 {page} 页成功，共 {len(pois)} 条数据")
                
                # 转换数据格式为GeoJSON Feature
                for item in pois:
                    location = item.get("location", "")
                    if not location:
                        continue
                        
                    lon, lat = map(float, location.split(","))
                    
                    feature = {
                        "type": "Feature",
                        "properties": {
                            "name": item.get("name"),
                            "address": item.get("address"),
                            "type": category, # 用于前端图标映射
                            "district": item.get("adname"),
                            "tel": item.get("tel", ""),
                            "biz_type": item.get("biz_type", [])
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        }
                    }
                    all_pois.append(feature)
                
                page += 1
                time.sleep(0.5) # 稍微暂停，避免触发频率限制
            else:
                print(f"  API返回错误: {data.get('info', 'Unknown error')}")
                break
                
        except Exception as e:
            print(f"  发生异常: {e}")
            break
            
    return all_pois

def save_to_geojson(features, category):
    """
    保存数据为GeoJSON文件
    """
    if not features:
        print(f"警告: [{category}] 类未获取到任何数据，跳过保存。")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(OUTPUT_DIR, f"{category}.geojson")
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        print(f"成功保存: {filename} (共 {len(features)} 条记录)\n")
    except Exception as e:
        print(f"保存文件失败: {e}\n")

def main():
    print("=== 开始从高德API获取真实POI数据 ===")
    print(f"API Key: {AMAP_KEY}")
    print("注意：如果遇到SSL错误，脚本已配置忽略证书验证。")
    print("----------------------------------------")
    
    for category, config in POI_CONFIG.items():
        features = fetch_pois_from_amap(category, config["keywords"], config["types"])
        save_to_geojson(features, category)
        
    print("=== 所有任务完成 ===")

if __name__ == "__main__":
    main()
