"""
空间分析接口
提供GIS空间分析功能：可达性分析、选址推荐、路线规划等
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json
from app.core.config import settings
from app.services.gis_service import GISService

router = APIRouter()
gis_service = GISService()


class RouteRequest(BaseModel):
    """路线规划请求模型"""
    start: List[float]  # [经度, 纬度]
    end: List[float]    # [经度, 纬度]
    waypoints: Optional[List[List[float]]] = None
    mode: str = "driving"  # 出行方式: driving, walking, cycling, transit


class SiteSelectionRequest(BaseModel):
    """选址分析请求模型"""
    facility_type: str  # 设施类型
    weights: Optional[dict] = None  # 各因子权重


class AccessibilityRequest(BaseModel):
    """可达性分析请求模型"""
    poi_type: str  # POI类型
    distance_threshold: int = 3000  # 距离阈值（米）


@router.post("/analysis/route")
async def plan_route(request: RouteRequest):
    """
    智能路线规划
    
    根据起点、终点和途经点规划最优路线
    支持多种出行方式: driving(驾车), walking(步行), cycling(骑行), transit(公交)
    """
    try:
        result = gis_service.plan_route(
            start=request.start,
            end=request.end,
            waypoints=request.waypoints,
            mode=request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analysis/site-selection")
async def site_selection(request: SiteSelectionRequest):
    """
    智能选址推荐
    
    使用加权叠加分析方法，根据多因子评估推荐最佳选址位置
    
    因子包括：
    - 人口密度
    - 交通便利度
    - 现有设施距离
    - 旅游热度
    """
    try:
        result = gis_service.site_selection(
            facility_type=request.facility_type,
            weights=request.weights
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analysis/accessibility")
async def accessibility_analysis(request: AccessibilityRequest):
    """
    可达性分析
    
    分析区域内到指定类型设施的可达性
    用于评估公共服务覆盖均衡性
    """
    try:
        result = gis_service.accessibility_analysis(
            poi_type=request.poi_type,
            threshold=request.distance_threshold
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/service-coverage")
async def service_coverage(
    poi_type: str = Query(..., description="POI类型: hospital, school"),
    buffer_distance: int = Query(2000, description="服务半径（米）")
):
    """
    公共服务覆盖分析
    
    计算指定类型设施的服务覆盖范围，
    识别服务盲区
    """
    try:
        result = gis_service.service_coverage(
            poi_type=poi_type,
            buffer_distance=buffer_distance
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/density")
async def density_analysis(
    poi_type: str = Query(..., description="POI类型"),
    cell_size: int = Query(1000, description="网格大小（米）")
):
    """
    密度分析
    
    生成POI分布的密度热力图数据
    """
    try:
        result = gis_service.density_analysis(
            poi_type=poi_type,
            cell_size=cell_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/tourism-route")
async def tourism_route_recommendation(
    theme: str = Query("mazu", description="旅游主题: mazu, scenic, culture"),
    duration: int = Query(1, description="游览天数")
):
    """
    妈祖文化旅游路线推荐
    
    根据主题和时间预算推荐最佳旅游路线
    """
    try:
        result = gis_service.tourism_route(
            theme=theme,
            duration=duration
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
