from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.get("/stats")
async def get_economy_stats():
    """
    获取莆田市经济产业统计数据 (2023-2024)
    数据来源：政府统计公报及官方媒体报道
    """
    return {
        "year": 2024,
        "total_gdp": 3442.74,  # 2024初步核算
        "gdp_growth": 12.1,    # 名义增长
        "gdp_per_capita": 108000, # 估算
        "description": "2024年莆田市地区生产总值(GDP)初步核算数",
        
        # 各区县数据 (2024/2023)
        "districts": [
            {
                "name": "城厢区",
                "gdp": 728.17, 
                "gdp_per_capita": 135000,
                "primary_industry": 1.5,
                "secondary_industry": 38.2, 
                "tertiary_industry": 60.3,
                "description": "现代服务业核心区，鞋服产业总部基地"
            },
            {
                "name": "涵江区",
                "gdp": 714.0, 
                "gdp_per_capita": 118000,
                "primary_industry": 4.5,
                "secondary_industry": 52.3,
                "tertiary_industry": 43.2,
                "description": "电子信息与食品加工产业集聚区（百威雪津）"
            },
            {
                "name": "荔城区",
                "gdp": 600.0, 
                "gdp_per_capita": 112000,
                "primary_industry": 3.8,
                "secondary_industry": 42.5,
                "tertiary_industry": 53.7,
                "description": "工艺美术与鞋服制造基地"
            },
            {
                "name": "秀屿区",
                "gdp": 545.0, 
                "gdp_per_capita": 105000,
                "primary_industry": 12.5,
                "secondary_industry": 55.6,
                "tertiary_industry": 31.9,
                "description": "临港工业、新型功能材料与能源基地"
            },
            {
                "name": "仙游县",
                "gdp": 795.0, 
                "gdp_per_capita": 68000,
                "primary_industry": 12.8,
                "secondary_industry": 45.2,
                "tertiary_industry": 42.0,
                "description": "中国古典工艺家具之都，工艺美术产业千亿县"
            }
        ],
        
        # 12条重点产业链
        "key_industries": [
            {
                "name": "鞋服产业",
                "value": 1400,
                "unit": "亿元",
                "growth": 5.2,
                "description": "首个千亿级产业集群，拥有‘莆田鞋’集体商标",
                "companies": ["双驰科技", "华峰华锦", "玩觅", "恒而达", "力奴鞋业"]
            },
            {
                "name": "工艺美术",
                "value": 750,
                "unit": "亿元",
                "growth": 6.8,
                "description": "仙游古典家具、莆田木雕、金银珠宝，目标千亿级",
                "companies": ["三福古典", "华昌珠宝", "四君子"]
            },
            {
                "name": "食品产业",
                "value": 550,
                "unit": "亿元",
                "growth": 4.5,
                "description": "以啤酒饮料、预制菜、海产品加工为主",
                "companies": ["百威雪津(亚洲最大)", "国圣食品", "方家铺子"]
            },
            {
                "name": "新型功能材料",
                "value": 650,
                "unit": "亿元",
                "growth": 10.4,
                "description": "突出发展鞋材、化工新材料、纤维材料",
                "companies": ["永荣科技(己内酰胺)", "三棵树涂料", "赛隆科技"]
            },
            {
                "name": "电子信息",
                "value": 400,
                "unit": "亿元",
                "growth": 3.4,
                "description": "集成电路、电子元器件、软件信息服务",
                "companies": ["福联集成电路", "安特微", "物泊科技"]
            },
            {
                "name": "高端装备",
                "value": 320,
                "unit": "亿元",
                "growth": 5.6,
                "description": "数控机床、激光切割、注塑机械",
                "companies": ["海安橡胶(巨型轮胎)", "荣兴机械"]
            }
        ],
        
        # 产业结构 (2023)
        "industry_structure": {
            "primary": 4.9,
            "secondary": 49.0,
            "tertiary": 46.1
        },
        
        "industrial_parks": [
            {"name": "涵江高新技术产业园", "type": "国家级", "focus": "电子信息、食品"},
            {"name": "秀屿临港工业园", "type": "省级", "focus": "化工、能源、木材加工"},
            {"name": "仙游经济开发区", "type": "省级", "focus": "工艺美术、鞋服"},
            {"name": "城厢经济开发区", "type": "省级", "focus": "鞋服制造、电子信息"}
        ]
    }
