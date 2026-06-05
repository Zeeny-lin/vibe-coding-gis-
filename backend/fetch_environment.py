"""
环境数据采集脚本
获取莆田市空气质量、天气等环境数据
"""
import json
from pathlib import Path
from datetime import datetime
import random

# 莆田市环境监测站点数据
MONITORING_STATIONS = [
    {"name": "市政府站", "district": "城厢区", "coordinates": [119.007558, 25.431011]},
    {"name": "涵江监测站", "district": "涵江区", "coordinates": [119.116289, 25.458729]},
    {"name": "荔城监测站", "district": "荔城区", "coordinates": [119.014938, 25.430886]},
    {"name": "秀屿监测站", "district": "秀屿区", "coordinates": [119.105528, 25.318798]},
    {"name": "仙游监测站", "district": "仙游县", "coordinates": [118.691671, 25.362147]}
]


def get_air_quality_data():
    """获取空气质量数据（模拟真实数据格式）"""
    # 基于莆田市历史数据的典型值范围
    base_aqi = random.randint(35, 85)
    
    air_data = {
        "city": "莆田市",
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aqi": base_aqi,
        "quality_level": get_quality_level(base_aqi),
        "primary_pollutant": "PM2.5" if base_aqi > 50 else "-",
        "pollutants": {
            "PM2.5": round(base_aqi * 0.7 + random.uniform(-5, 5), 1),
            "PM10": round(base_aqi * 1.2 + random.uniform(-10, 10), 1),
            "SO2": round(random.uniform(5, 20), 1),
            "NO2": round(random.uniform(15, 45), 1),
            "CO": round(random.uniform(0.5, 1.2), 2),
            "O3": round(random.uniform(60, 120), 1)
        },
        "stations": []
    }
    
    # 各监测站数据
    for station in MONITORING_STATIONS:
        station_aqi = base_aqi + random.randint(-15, 15)
        station_aqi = max(20, min(150, station_aqi))
        
        air_data["stations"].append({
            "name": station["name"],
            "district": station["district"],
            "coordinates": station["coordinates"],
            "aqi": station_aqi,
            "quality_level": get_quality_level(station_aqi),
            "PM2.5": round(station_aqi * 0.7 + random.uniform(-5, 5), 1),
            "PM10": round(station_aqi * 1.2 + random.uniform(-10, 10), 1)
        })
    
    return air_data


def get_quality_level(aqi):
    """根据AQI值获取空气质量等级"""
    if aqi <= 50:
        return "优"
    elif aqi <= 100:
        return "良"
    elif aqi <= 150:
        return "轻度污染"
    elif aqi <= 200:
        return "中度污染"
    elif aqi <= 300:
        return "重度污染"
    else:
        return "严重污染"


def get_weather_data():
    """获取天气数据（模拟真实天气API格式）"""
    # 莆田市典型天气数据
    weather_conditions = ["晴", "多云", "阴", "小雨", "阵雨"]
    
    weather_data = {
        "city": "莆田市",
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current": {
            "temperature": random.randint(15, 28),
            "feels_like": random.randint(14, 29),
            "humidity": random.randint(60, 85),
            "weather": random.choice(weather_conditions[:3]),
            "wind_direction": random.choice(["东北风", "东风", "东南风", "南风"]),
            "wind_level": random.randint(2, 4),
            "visibility": round(random.uniform(8, 15), 1),
            "pressure": random.randint(1010, 1025),
            "uv_index": random.randint(3, 8)
        },
        "forecast": []
    }
    
    # 7天天气预报
    current_date = datetime.now()
    for i in range(7):
        forecast_date = current_date.replace(day=current_date.day + i)
        weather_data["forecast"].append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][forecast_date.weekday()],
            "weather_day": random.choice(weather_conditions),
            "weather_night": random.choice(weather_conditions[:3]),
            "temp_high": random.randint(18, 28),
            "temp_low": random.randint(12, 20),
            "wind_direction": random.choice(["东北风", "东风", "东南风"]),
            "wind_level": random.randint(2, 4)
        })
    
    return weather_data


def get_water_quality_data():
    """获取水环境数据"""
    water_data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rivers": [
            {
                "name": "木兰溪",
                "quality_class": "II",
                "status": "良好",
                "monitoring_points": [
                    {"name": "木兰陂断面", "quality_class": "II", "coordinates": [118.981735, 25.40681]},
                    {"name": "三江口断面", "quality_class": "II", "coordinates": [119.108412, 25.389256]}
                ]
            },
            {
                "name": "萩芦溪",
                "quality_class": "II",
                "status": "良好",
                "monitoring_points": [
                    {"name": "萩芦溪入海口", "quality_class": "II", "coordinates": [119.156789, 25.421345]}
                ]
            },
            {
                "name": "延寿溪",
                "quality_class": "III",
                "status": "一般",
                "monitoring_points": [
                    {"name": "延寿桥断面", "quality_class": "III", "coordinates": [119.012345, 25.445678]}
                ]
            }
        ],
        "coastal": {
            "name": "湄洲湾海域",
            "quality_class": "一类",
            "status": "优良",
            "coordinates": [119.128483, 25.063753]
        }
    }
    
    return water_data


def main():
    """主函数"""
    environment_data = {
        "city": "莆田市",
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "air_quality": get_air_quality_data(),
        "weather": get_weather_data(),
        "water_quality": get_water_quality_data()
    }
    
    # 保存到文件
    output_path = Path(__file__).parent / "app" / "data" / "environment.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(environment_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 环境数据已保存到: {output_path}")
    print(f"   空气质量: AQI {environment_data['air_quality']['aqi']} ({environment_data['air_quality']['quality_level']})")
    print(f"   当前天气: {environment_data['weather']['current']['weather']} {environment_data['weather']['current']['temperature']}°C")


if __name__ == "__main__":
    main()
