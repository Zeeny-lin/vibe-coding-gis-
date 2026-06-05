"""
交通数据接口
提供莆田市铁路、公路、港口等交通基础设施数据
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from app.core.config import settings

router = APIRouter()


def load_transport_data():
    """加载交通数据"""
    data_file = settings.DATA_DIR / "transport.json"
    if not data_file.exists():
        return None
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_transport_geojson():
    """加载交通设施GeoJSON"""
    features = []
    
    # Load original point data (Stations, Ports)
    data_file = settings.DATA_DIR / "poi" / "transport.geojson"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            features.extend(data.get("features", []))
            
    # Load real vector data (Railways, Highways)
    real_data_file = settings.DATA_DIR / "poi" / "transport_real.geojson"
    if real_data_file.exists():
        with open(real_data_file, "r", encoding="utf-8") as f:
            real_data = json.load(f)
            features.extend(real_data.get("features", []))
            
    if not features:
        return None
        
    return {
        "type": "FeatureCollection",
        "features": features
    }


@router.get("/transport")
async def get_all_transport():
    """
    获取所有交通数据
    
    包含铁路、公路、港口等交通基础设施信息
    """
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return data


@router.get("/transport/railway")
async def get_railway():
    """获取铁路数据"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return data.get("railway", {})


@router.get("/transport/highway")
async def get_highway():
    """获取公路数据"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return data.get("highway", {})


@router.get("/transport/port")
async def get_ports():
    """获取港口数据"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return data.get("port", {})


@router.get("/transport/geojson")
async def get_transport_geojson():
    """获取交通设施GeoJSON数据（用于地图展示）"""
    data = load_transport_geojson()
    if data is None:
        raise HTTPException(status_code=404, detail="交通GeoJSON数据未找到")
    return data


@router.get("/transport/statistics")
async def get_transport_stats():
    """获取交通统计数据"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return data.get("statistics", {})


@router.get("/transport/schedules/train")
async def get_train_schedules():
    """获取火车班次时刻表"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return {
        "schedules": data.get("railway", {}).get("schedules", []),
        "stations": data.get("railway", {}).get("stations", [])
    }


@router.get("/transport/schedules/ferry")
async def get_ferry_schedules():
    """获取轮渡班次时刻表"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    return {
        "schedules": data.get("port", {}).get("ferry_schedules", []),
        "ports": data.get("port", {}).get("ports", [])
    }


@router.get("/transport/schedules/bus")
async def get_bus_schedules():
    """获取长途汽车班次时刻表"""
    data = load_transport_data()
    if data is None:
        raise HTTPException(status_code=404, detail="交通数据未找到")
    bus_data = data.get("bus_station", {})
    return {
        "schedules": bus_data.get("intercity_schedules", []),
        "stations": bus_data.get("stations", [])
    }
