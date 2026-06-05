"""
POI兴趣点数据接口
提供莆田市各类POI数据（医院、学校、景点、妈祖庙等）
"""
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional, List
import json
from app.core.config import settings

router = APIRouter()

# POI类型枚举
POI_TYPES = {
    "hospital": "医疗机构",
    "school": "教育机构", 
    "scenic": "风景名胜",
    "mazu": "妈祖文化",
    "hotel": "住宿服务",
    "restaurant": "餐饮美食"
}


def load_poi_data(poi_type: str = None):
    """加载POI数据"""
    poi_dir = settings.DATA_DIR / "poi"
    
    if poi_type:
        # 加载特定类型的POI
        data_file = poi_dir / f"{poi_type}.geojson"
        if not data_file.exists():
            return None
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 加载所有POI
        all_features = []
        if poi_dir.exists():
            for file in poi_dir.glob("*.geojson"):
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_features.extend(data.get("features", []))
        return {
            "type": "FeatureCollection",
            "features": all_features
        }


@router.get("/poi")
async def get_all_poi(
    type: Optional[str] = Query(None, description="POI类型: hospital, school, scenic, mazu, hotel, restaurant"),
    district: Optional[str] = Query(None, description="区县名称过滤")
):
    """
    获取POI兴趣点数据
    
    可选参数:
    - **type**: POI类型过滤
    - **district**: 按区县名称过滤
    """
    data = load_poi_data(type)
    if data is None:
        raise HTTPException(status_code=404, detail=f"POI数据未找到: {type}")
    
    # 如果指定了区县，进行过滤
    if district:
        filtered_features = [
            f for f in data.get("features", [])
            if f.get("properties", {}).get("district") == district
        ]
        data = {
            "type": "FeatureCollection",
            "features": filtered_features
        }
    
    return data


@router.get("/poi/types")
async def get_poi_types():
    """获取所有POI类型列表"""
    return {"types": POI_TYPES}


@router.get("/poi/stats")
async def get_poi_statistics():
    """获取各类型POI的统计数量"""
    poi_dir = settings.DATA_DIR / "poi"
    stats = {}
    
    if poi_dir.exists():
        for file in poi_dir.glob("*.geojson"):
            poi_type = file.stem
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                count = len(data.get("features", []))
                stats[poi_type] = {
                    "name": POI_TYPES.get(poi_type, poi_type),
                    "count": count
                }
    
    return {"statistics": stats}


@router.get("/poi/scenic-areas")
async def get_scenic_areas():
    """获取景区范围多边形数据"""
    poi_dir = settings.DATA_DIR / "poi"
    data_file = poi_dir / "scenic_areas.geojson"
    
    if not data_file.exists():
        return {
            "type": "FeatureCollection",
            "features": []
        }
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/poi/{poi_id}")
async def get_poi_by_id(poi_id: str):
    """根据POI ID获取详细信息"""
    data = load_poi_data()
    
    for feature in data.get("features", []):
        if feature.get("properties", {}).get("id") == poi_id:
            return feature
    
    raise HTTPException(status_code=404, detail=f"未找到POI: {poi_id}")
