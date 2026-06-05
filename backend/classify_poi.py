"""
POI数据分类脚本
为医院和学校数据添加等级分类
"""
import json
import os
import re

# 医院等级分类规则
HOSPITAL_LEVELS = {
    '三甲': ['第一医院', '附属医院', '人民医院', '中心医院', '总医院', '九十五医院', '协和医院'],
    '二甲': ['第二医院', '第三医院', '第四医院', '区医院', '县医院', '中医医院', '中医院', '妇幼保健院'],
    '一级': ['卫生院', '社区卫生', '乡镇卫生'],
    '专科': ['口腔', '眼科', '妇产', '骨科', '康复', '精神', '皮肤', '儿童', '肿瘤', '心血管', '生殖']
}

# 学校等级分类规则
SCHOOL_LEVELS = {
    '大学': ['大学', '学院', '职业技术学院', '高等专科'],
    '高中': ['高级中学', '高中', '一中', '二中', '三中', '四中', '五中', '六中', '中学'],
    '初中': ['初级中学', '初中'],
    '小学': ['小学', '实验小学'],
    '职校': ['职业学校', '职校', '技校', '技术学校', '工业学校', '卫生学校', '师范学校'],
    '幼儿园': ['幼儿园', '托儿所']
}


def classify_hospital(name):
    """根据医院名称判断等级"""
    # 先检查专科
    for keyword in HOSPITAL_LEVELS['专科']:
        if keyword in name:
            return '专科医院'
    
    # 检查三甲
    for keyword in HOSPITAL_LEVELS['三甲']:
        if keyword in name:
            return '三甲医院'
    
    # 检查二甲
    for keyword in HOSPITAL_LEVELS['二甲']:
        if keyword in name:
            return '二甲医院'
    
    # 检查一级
    for keyword in HOSPITAL_LEVELS['一级']:
        if keyword in name:
            return '一级医院'
    
    # 默认为综合医院
    return '综合医院'


def classify_school(name):
    """根据学校名称判断类型"""
    # 检查大学
    for keyword in SCHOOL_LEVELS['大学']:
        if keyword in name:
            return '高等院校'
    
    # 检查职校（优先于中学判断）
    for keyword in SCHOOL_LEVELS['职校']:
        if keyword in name:
            return '职业学校'
    
    # 检查高中
    # 使用更精确的匹配
    if re.search(r'第?(一|二|三|四|五|六|七|八|九|十|[0-9]+)中学?$', name) or '高中' in name or '高级中学' in name:
        return '高中'
    
    # 检查初中
    if '初级中学' in name or '初中' in name:
        return '初中'
    
    # 检查中学（既不是高中也不是初中的，归类为中学）
    if '中学' in name:
        return '中学'
    
    # 检查小学
    for keyword in SCHOOL_LEVELS['小学']:
        if keyword in name:
            return '小学'
    
    # 检查幼儿园
    for keyword in SCHOOL_LEVELS['幼儿园']:
        if keyword in name:
            return '幼儿园'
    
    return '其他学校'


def process_hospital_data(input_path, output_path):
    """处理医院数据，添加等级分类"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    level_stats = {}
    for feature in data['features']:
        name = feature['properties'].get('name', '')
        level = classify_hospital(name)
        feature['properties']['level'] = level
        level_stats[level] = level_stats.get(level, 0) + 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"医院分类完成，共 {len(data['features'])} 条记录")
    for level, count in sorted(level_stats.items(), key=lambda x: -x[1]):
        print(f"  {level}: {count}")
    return level_stats


def process_school_data(input_path, output_path):
    """处理学校数据，添加类型分类"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    level_stats = {}
    for feature in data['features']:
        name = feature['properties'].get('name', '')
        level = classify_school(name)
        feature['properties']['level'] = level
        level_stats[level] = level_stats.get(level, 0) + 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"学校分类完成，共 {len(data['features'])} 条记录")
    for level, count in sorted(level_stats.items(), key=lambda x: -x[1]):
        print(f"  {level}: {count}")
    return level_stats


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    poi_dir = os.path.join(base_dir, 'app', 'data', 'poi')
    
    print("=" * 50)
    print("开始处理POI数据分类...")
    print("=" * 50)
    
    # 处理医院数据
    hospital_path = os.path.join(poi_dir, 'hospital.geojson')
    if os.path.exists(hospital_path):
        print("\n处理医院数据...")
        process_hospital_data(hospital_path, hospital_path)
    else:
        print(f"未找到医院数据文件: {hospital_path}")
    
    # 处理学校数据
    school_path = os.path.join(poi_dir, 'school.geojson')
    if os.path.exists(school_path):
        print("\n处理学校数据...")
        process_school_data(school_path, school_path)
    else:
        print(f"未找到学校数据文件: {school_path}")
    
    print("\n" + "=" * 50)
    print("POI数据分类完成!")
    print("=" * 50)
