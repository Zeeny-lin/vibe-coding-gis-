"""
莆田市房产数据生成脚本
生成1000+条房产数据，坐标使用GCJ-02（高德坐标系）
"""
import json
import random
import os

# 莆田市各区县边界（GCJ-02坐标系，与高德地图匹配）
DISTRICTS = {
    '城厢区': {
        'center': [119.0017, 25.4343],
        'bbox': [118.95, 25.38, 119.05, 25.50],
        'avg_price': 12500,
        'communities': ['正荣润城', '万科城', '融创壹号院', '保利城', '绿地新都会', '碧桂园天玺', '恒大城', '龙德井小区', '荔园小区', '文献步行街']
    },
    '荔城区': {
        'center': [119.0264, 25.4329],
        'bbox': [118.98, 25.38, 119.08, 25.50],
        'avg_price': 13500,
        'communities': ['正荣财富中心', '万达广场', '联创国际广场', '涵华世纪城', '荔景新城', '荔能华景', '阳光城', '中海城', '金鼎国际', '荔城壹号']
    },
    '涵江区': {
        'center': [119.1163, 25.4588],
        'bbox': [119.05, 25.40, 119.18, 25.52],
        'avg_price': 10500,
        'communities': ['兴涵水都', '涵江万达', '白塘名邸', '三江口', '涵城水岸', '华永天澜城', '国欢镇新村', '楼下社区', '高新园区', '港口新城']
    },
    '秀屿区': {
        'center': [119.1054, 25.3184],
        'bbox': [119.03, 25.22, 119.20, 25.38],
        'avg_price': 8500,
        'communities': ['笏石新城', '秀屿港城', '埭头镇区', '平海镇区', '南日岛', '月塘新区', '东庄镇区', '忠门镇区', '湄洲湾新城', '东峤镇']
    },
    '仙游县': {
        'center': [118.6919, 25.3620],
        'bbox': [118.55, 25.25, 118.85, 25.50],
        'avg_price': 7500,
        'communities': ['鲤城步行街', '木兰溪畔', '榜头镇区', '度尾镇区', '大济镇区', '龙华镇区', '园庄镇区', '枫亭镇', '盖尾镇', '郊尾镇']
    }
}

# 房屋类型
HOUSE_TYPES = [
    {'type': '两室一厅', 'area_range': (65, 95), 'weight': 3},
    {'type': '三室两厅', 'area_range': (90, 140), 'weight': 4},
    {'type': '四室两厅', 'area_range': (130, 180), 'weight': 2},
    {'type': '一室一厅', 'area_range': (40, 65), 'weight': 1},
    {'type': '复式', 'area_range': (150, 250), 'weight': 1}
]

# 装修类型
DECORATIONS = ['毛坯', '简装', '精装', '豪装']
DECORATION_WEIGHTS = [2, 3, 4, 1]

# 朝向
ORIENTATIONS = ['南', '南北', '东南', '西南', '东', '西']

def generate_housing_data(count=1200):
    """生成房产数据"""
    features = []
    
    for i in range(count):
        # 随机选择区县
        district = random.choice(list(DISTRICTS.keys()))
        district_info = DISTRICTS[district]
        
        # 生成坐标（在区县范围内随机）
        bbox = district_info['bbox']
        lng = random.uniform(bbox[0], bbox[2])
        lat = random.uniform(bbox[1], bbox[3])
        
        # 选择小区
        community = random.choice(district_info['communities'])
        
        # 选择房屋类型
        house_type_info = random.choices(HOUSE_TYPES, weights=[h['weight'] for h in HOUSE_TYPES])[0]
        house_type = house_type_info['type']
        area = round(random.uniform(*house_type_info['area_range']), 1)
        
        # 计算价格（基于区域均价、面积和随机波动）
        base_price = district_info['avg_price']
        price_factor = random.uniform(0.8, 1.3)  # 价格波动
        unit_price = round(base_price * price_factor)
        total_price = round(unit_price * area / 10000, 2)  # 总价（万元）
        
        # 其他属性
        floor = random.randint(1, 32)
        total_floors = random.randint(max(floor, 6), 33)
        year = random.randint(2005, 2024)
        decoration = random.choices(DECORATIONS, weights=DECORATION_WEIGHTS)[0]
        orientation = random.choice(ORIENTATIONS)
        
        # 生成名称
        name = f"{community}{random.randint(1, 20)}栋{floor}{random.randint(1, 4):02d}"
        
        feature = {
            'type': 'Feature',
            'properties': {
                'id': f'house_{i+1:05d}',
                'name': name,
                'type': 'housing',
                'district': district,
                'community': community,
                'house_type': house_type,
                'area': area,
                'unit_price': unit_price,
                'total_price': total_price,
                'floor': f'{floor}/{total_floors}层',
                'year': year,
                'decoration': decoration,
                'orientation': orientation
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [round(lng, 6), round(lat, 6)]
            }
        }
        features.append(feature)
    
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def analyze_housing_data(data):
    """分析房产数据"""
    features = data['features']
    
    # 按区县统计
    district_stats = {}
    for f in features:
        props = f['properties']
        district = props['district']
        if district not in district_stats:
            district_stats[district] = {
                'count': 0,
                'total_area': 0,
                'total_price_sum': 0,
                'prices': []
            }
        district_stats[district]['count'] += 1
        district_stats[district]['total_area'] += props['area']
        district_stats[district]['total_price_sum'] += props['total_price']
        district_stats[district]['prices'].append(props['unit_price'])
    
    print("\n" + "=" * 50)
    print("房产数据统计分析")
    print("=" * 50)
    print(f"\n总计生成: {len(features)} 条房产数据\n")
    
    print("各区县统计:")
    print("-" * 50)
    for district, stats in sorted(district_stats.items(), key=lambda x: -x[1]['count']):
        avg_price = sum(stats['prices']) / len(stats['prices'])
        avg_area = stats['total_area'] / stats['count']
        print(f"  {district}: {stats['count']}套, 均价{avg_price:.0f}元/㎡, 均面积{avg_area:.1f}㎡")
    
    # 按户型统计
    type_stats = {}
    for f in features:
        house_type = f['properties']['house_type']
        if house_type not in type_stats:
            type_stats[house_type] = 0
        type_stats[house_type] += 1
    
    print("\n户型分布:")
    print("-" * 50)
    for house_type, count in sorted(type_stats.items(), key=lambda x: -x[1]):
        print(f"  {house_type}: {count}套 ({count/len(features)*100:.1f}%)")
    
    return district_stats


if __name__ == '__main__':
    print("开始生成莆田市房产数据...")
    
    # 生成数据
    housing_data = generate_housing_data(1200)
    
    # 分析数据
    analyze_housing_data(housing_data)
    
    # 保存数据
    output_dir = os.path.join(os.path.dirname(__file__), 'app', 'data', 'poi')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'housing.geojson')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(housing_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    print("=" * 50)
