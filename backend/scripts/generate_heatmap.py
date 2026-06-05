import json
import random
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "app" / "data"
POI_DIR = DATA_DIR / "poi"
OUTPUT_FILE = DATA_DIR / "population_heatmap.json"

# 权重配置
WEIGHTS = {
    "housing.geojson": {"count": 5, "intensity": 0.8, "spread": 0.005}, # 居住区：高密度
    "school.geojson": {"count": 8, "intensity": 0.9, "spread": 0.003},  # 学校：高聚集
    "hospital.geojson": {"count": 10, "intensity": 0.9, "spread": 0.003}, # 医院：高聚集
    "government.geojson": {"count": 5, "intensity": 0.7, "spread": 0.002} # 政府：中聚集
}

# 兜底区域中心（如果POI数据不足）
DISTRICT_CENTERS = {
    "城厢区": [25.433, 118.99],
    "荔城区": [25.431, 119.01],
    "涵江区": [25.459, 119.11],
    "秀屿区": [25.266, 119.08],
    "仙游县": [25.363, 118.69]
}

def load_geojson_points(filename):
    file_path = POI_DIR / filename
    points = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for feature in data.get("features", []):
                    # 获取坐标 (GeoJSON 通常是 [lng, lat])
                    geom = feature.get("geometry", {})
                    coord = geom.get("coordinates")
                    if coord and geom.get("type") == "Point":
                        points.append([coord[1], coord[0]]) # 转为 [lat, lng]
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    return points

def generate_heat_points():
    heat_points = []
    
    # 1.基于真实POI生成热力点
    for filename, config in WEIGHTS.items():
        base_points = load_geojson_points(filename)
        print(f"Loaded {len(base_points)} points from {filename}")
        
        for p in base_points:
            # 在每个POI周围生成一簇点
            for _ in range(config["count"]):
                # 添加高斯噪点模拟周边分布
                lat = p[0] + random.gauss(0, config["spread"])
                lng = p[1] + random.gauss(0, config["spread"])
                # 强度随机浮动
                intensity = min(config["intensity"] * random.uniform(0.8, 1.2), 1.0)
                heat_points.append([lat, lng, intensity])

    # 2. 如果点太少(说明没抓取到POI)，回退到基于区县中心的生成模式
    if len(heat_points) < 1000:
        print("POI data insufficient, adding fallback center points...")
        for name, center in DISTRICT_CENTERS.items():
            for _ in range(800):
                lat = center[0] + random.gauss(0, 0.03)
                lng = center[1] + random.gauss(0, 0.03)
                heat_points.append([lat, lng, random.uniform(0.3, 0.8)])
    
    return heat_points

def main():
    print("Generating structured population heatmap data from POIs...")
    points = generate_heat_points()
    
    # 2024年真实数据
    result = {
        "year": 2024,
        "total_population": 319.2,
        "districts": [
            { "name": "城厢区", "population": 54.42, "population_density": 1200, "urban_rate": 88.5 },
            { "name": "荔城区", "population": 67.01, "population_density": 2300, "urban_rate": 93.5 },
            { "name": "涵江区", "population": 47.60, "population_density": 780, "urban_rate": 74.2 },
            { "name": "秀屿区", "population": 60.07, "population_density": 710, "urban_rate": 60.2 },
            { "name": "仙游县", "population": 90.10, "population_density": 480, "urban_rate": 54.1 }
        ],
        "heatmap_points": points
    }
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(points)} structured heat points.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
