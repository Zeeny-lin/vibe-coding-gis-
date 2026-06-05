"""
行政区划数据接口
提供莆田市及下辖区县的边界数据
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from app.core.config import settings

router = APIRouter()


def load_districts_data():
    """加载行政区划GeoJSON数据"""
    data_file = settings.DATA_DIR / "districts.geojson"
    if not data_file.exists():
        return None
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/districts")
async def get_districts():
    """
    获取莆田市行政区划数据
    
    返回莆田市及下辖5个区县（城厢区、涵江区、荔城区、秀屿区、仙游县）的边界GeoJSON数据
    """
    data = load_districts_data()
    if data is None:
        raise HTTPException(status_code=404, detail="行政区划数据未找到")
    return data


@router.get("/districts/{district_name}")
async def get_district_by_name(district_name: str):
    """
    根据区县名称获取单个区县的边界数据
    
    - **district_name**: 区县名称，如"城厢区"、"涵江区"等
    """
    data = load_districts_data()
    if data is None:
        raise HTTPException(status_code=404, detail="行政区划数据未找到")
    
    # 在FeatureCollection中查找匹配的区县
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        if props.get("name") == district_name or props.get("name", "").startswith(district_name):
            return {
                "type": "FeatureCollection",
                "features": [feature]
            }
    
    raise HTTPException(status_code=404, detail=f"未找到区县: {district_name}")


@router.get("/districts/list/names")
async def get_district_names():
    """获取所有区县名称列表"""
    data = load_districts_data()
    if data is None:
        raise HTTPException(status_code=404, detail="行政区划数据未找到")
    
    names = []
    for feature in data.get("features", []):
        name = feature.get("properties", {}).get("name")
        if name:
            names.append(name)
    
    return {"districts": names, "count": len(names)}
