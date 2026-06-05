"""
政府驻地数据采集脚本
获取莆田市各区县政府驻地坐标
"""
import json
from pathlib import Path

# 莆田市各区县政府驻地数据（基于官方公开信息）
GOVERNMENT_DATA = [
    {
        "name": "莆田市人民政府",
        "address": "城厢区荔城中大道2169号",
        "district": "城厢区",
        "level": "市级",
        "coordinates": [119.007558, 25.431011],
        "tel": "0594-2684116"
    },
    {
        "name": "城厢区人民政府",
        "address": "城厢区文献西路16号",
        "district": "城厢区",
        "level": "区级",
        "coordinates": [119.003367, 25.441967],
        "tel": "0594-2293291"
    },
    {
        "name": "涵江区人民政府",
        "address": "涵江区涵东街道涵华东路369号",
        "district": "涵江区",
        "level": "区级",
        "coordinates": [119.116289, 25.458729],
        "tel": "0594-3362218"
    },
    {
        "name": "荔城区人民政府",
        "address": "荔城区胜利北街239号",
        "district": "荔城区",
        "level": "区级",
        "coordinates": [119.014938, 25.430886],
        "tel": "0594-2293368"
    },
    {
        "name": "秀屿区人民政府",
        "address": "秀屿区笏石镇秀屿大道88号",
        "district": "秀屿区",
        "level": "区级",
        "coordinates": [119.105528, 25.318798],
        "tel": "0594-5857003"
    },
    {
        "name": "仙游县人民政府",
        "address": "仙游县鲤城街道八二五大街1号",
        "district": "仙游县",
        "level": "县级",
        "coordinates": [118.691671, 25.362147],
        "tel": "0594-8592503"
    }
]


def create_geojson():
    """生成政府驻地GeoJSON数据"""
    features = []
    
    for gov in GOVERNMENT_DATA:
        feature = {
            "type": "Feature",
            "properties": {
                "name": gov["name"],
                "address": gov["address"],
                "type": "government",
                "district": gov["district"],
                "level": gov["level"],
                "tel": gov["tel"],
                "biz_type": "gov"
            },
            "geometry": {
                "type": "Point",
                "coordinates": gov["coordinates"]
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson


def main():
    """主函数"""
    # 生成GeoJSON
    geojson_data = create_geojson()
    
    # 保存到文件
    output_path = Path(__file__).parent / "app" / "data" / "poi" / "government.geojson"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 政府驻地数据已保存到: {output_path}")
    print(f"   共 {len(GOVERNMENT_DATA)} 个政府机构")


if __name__ == "__main__":
    main()
