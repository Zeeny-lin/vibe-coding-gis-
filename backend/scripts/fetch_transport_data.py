# -*- coding: utf-8 -*-
"""
交通数据爬取脚本
使用高德地图API获取莆田市真实交通数据
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
from pathlib import Path
from datetime import datetime

# 设置标准输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

AMAP_KEY = os.getenv('AMAP_API_KEY')
DATA_DIR = Path(__file__).parent.parent / "app" / "data"

# SSL配置
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def amap_request(url):
    """发送高德API请求"""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as response:
        return json.loads(response.read().decode('utf-8'))


def fetch_bus_stations():
    """获取莆田市汽车站信息"""
    print("正在获取汽车站数据...")
    
    # 高德POI搜索 - 汽车站
    keywords = "汽车站|客运站|长途汽车站"
    city = "莆田"
    url = f"https://restapi.amap.com/v3/place/text?keywords={urllib.parse.quote(keywords)}&city={urllib.parse.quote(city)}&output=json&offset=20&key={AMAP_KEY}"
    
    data = amap_request(url)
    
    stations = []
    if data.get('status') == '1' and data.get('pois'):
        for poi in data['pois']:
            loc = poi.get('location', '').split(',')
            if len(loc) == 2:
                stations.append({
                    "name": poi.get('name'),
                    "address": poi.get('address', ''),
                    "coordinates": [float(loc[0]), float(loc[1])],
                    "tel": poi.get('tel', '')
                })
    
    print(f"  找到 {len(stations)} 个汽车站")
    return stations


def fetch_train_stations():
    """获取莆田市火车站信息"""
    print("正在获取火车站数据...")
    
    keywords = "火车站|高铁站"
    city = "莆田"
    url = f"https://restapi.amap.com/v3/place/text?keywords={urllib.parse.quote(keywords)}&city={urllib.parse.quote(city)}&output=json&offset=10&key={AMAP_KEY}"
    
    data = amap_request(url)
    
    stations = []
    if data.get('status') == '1' and data.get('pois'):
        for poi in data['pois']:
            loc = poi.get('location', '').split(',')
            if len(loc) == 2:
                stations.append({
                    "name": poi.get('name'),
                    "address": poi.get('address', ''),
                    "coordinates": [float(loc[0]), float(loc[1])],
                    "type": "高铁站" if "高铁" in poi.get('name', '') else "火车站"
                })
    
    print(f"  找到 {len(stations)} 个火车站")
    return stations


def fetch_ports():
    """获取莆田市港口码头信息"""
    print("正在获取港口码头数据...")
    
    keywords = "码头|港口|客运港"
    city = "莆田"
    url = f"https://restapi.amap.com/v3/place/text?keywords={urllib.parse.quote(keywords)}&city={urllib.parse.quote(city)}&output=json&offset=20&key={AMAP_KEY}"
    
    data = amap_request(url)
    
    ports = []
    if data.get('status') == '1' and data.get('pois'):
        for poi in data['pois']:
            loc = poi.get('location', '').split(',')
            if len(loc) == 2:
                port_type = "客运码头" if "客运" in poi.get('name', '') or "文甲" in poi.get('name', '') else "货运港口"
                ports.append({
                    "name": poi.get('name'),
                    "type": port_type,
                    "coordinates": [float(loc[0]), float(loc[1])],
                    "district": poi.get('adname', ''),
                    "address": poi.get('address', '')
                })
    
    print(f"  找到 {len(ports)} 个港口码头")
    return ports


def fetch_bus_lines():
    """获取莆田市公交线路信息"""
    print("正在获取公交线路数据...")
    
    # 获取一些主要公交线路
    lines = []
    key_routes = ["K1", "K2", "21", "23", "32", "36", "39", "101", "201", "301"]
    
    for route in key_routes:
        keywords = urllib.parse.quote(f"{route}路")
        url = f"https://restapi.amap.com/v3/bus/linename?keywords={keywords}&city=%E8%8E%86%E7%94%B0&output=json&key={AMAP_KEY}"
        try:
            data = amap_request(url)
            if data.get('status') == '1' and data.get('buslines'):
                busline = data['buslines'][0]
                lines.append({
                    "name": busline.get('name', f'{route}路'),
                    "start_stop": busline.get('start_stop', ''),
                    "end_stop": busline.get('end_stop', ''),
                    "distance": busline.get('distance', ''),
                    "basic_price": busline.get('basic_price', '2'),
                    "total_price": busline.get('total_price', '2')
                })
        except Exception as e:
            print(f"  获取 {route}路 失败: {e}")
    
    print(f"  找到 {len(lines)} 条公交线路")
    return lines


def update_transport_json():
    """更新transport.json文件"""
    transport_file = DATA_DIR / "transport.json"
    
    # 读取现有数据
    with open(transport_file, 'r', encoding='utf-8') as f:
        transport_data = json.load(f)
    
    # 获取新数据
    new_train_stations = fetch_train_stations()
    new_bus_stations = fetch_bus_stations()
    new_ports = fetch_ports()
    new_bus_lines = fetch_bus_lines()
    
    # 更新火车站坐标（保留现有的详细信息，只更新坐标）
    if new_train_stations:
        station_coords = {s['name']: s['coordinates'] for s in new_train_stations}
        for station in transport_data.get('railway', {}).get('stations', []):
            for name, coords in station_coords.items():
                if station['name'] in name or name in station['name']:
                    station['coordinates'] = coords
                    print(f"  更新 {station['name']} 坐标: {coords}")
                    break
    
    # 更新汽车站信息
    if new_bus_stations:
        transport_data['bus_station']['stations'] = new_bus_stations[:5]  # 保留前5个
    
    # 更新港口信息（保留现有详细信息，更新坐标）
    if new_ports:
        port_coords = {p['name']: p['coordinates'] for p in new_ports}
        for port in transport_data.get('port', {}).get('ports', []):
            for name, coords in port_coords.items():
                if port['name'] in name or name in port['name']:
                    port['coordinates'] = coords
                    print(f"  更新 {port['name']} 坐标: {coords}")
                    break
    
    # 更新公交线路信息
    if new_bus_lines:
        transport_data['public_transport']['key_routes'] = [
            {"name": line['name'], "description": f"{line['start_stop']} - {line['end_stop']}"}
            for line in new_bus_lines
        ]
        transport_data['public_transport']['bus_lines'] = len(new_bus_lines) * 7  # 估算
    
    # 更新时间戳
    transport_data['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    transport_data['data_source'] = "高德地图API"
    
    # 保存更新后的数据
    with open(transport_file, 'w', encoding='utf-8') as f:
        json.dump(transport_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 已更新 {transport_file}")
    print(f"  更新时间: {transport_data['update_time']}")


def main():
    if not AMAP_KEY:
        print("错误: 未找到 AMAP_API_KEY 环境变量")
        print("请在 .env 文件中配置高德API密钥")
        return
    
    print("=" * 50)
    print("莆田市交通数据更新工具")
    print("=" * 50)
    print(f"使用高德API密钥: {AMAP_KEY[:8]}...")
    print()
    
    update_transport_json()
    
    print()
    print("=" * 50)
    print("数据更新完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
