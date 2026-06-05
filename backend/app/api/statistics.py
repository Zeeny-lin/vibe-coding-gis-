"""
统计数据接口
提供莆田市人口、经济、资源等统计数据
"""
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional
import json
import csv
from app.core.config import settings

router = APIRouter()


def load_statistics_data():
    """加载统计数据"""
    data_file = settings.DATA_DIR / "statistics.json"
    if not data_file.exists():
        return None
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/statistics")
async def get_all_statistics():
    """
    获取所有统计数据
    
    包含各区县的人口、经济、医疗、教育等综合指标
    """
    data = load_statistics_data()
    if data is None:
        raise HTTPException(status_code=404, detail="统计数据未找到")
    return data


@router.get("/statistics/population")
async def get_population_statistics():
    """获取人口统计数据（含热力图数据）"""
    # 尝试加载真实人口数据（含热力图）
    heatmap_file = settings.DATA_DIR / "population_heatmap.json"
    if heatmap_file.exists():
        with open(heatmap_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback to statistics.json
    data = load_statistics_data()
    if data is None:
        raise HTTPException(status_code=404, detail="统计数据未找到")
    
    population_data = []
    for district in data.get("districts", []):
        population_data.append({
            "name": district.get("name"),
            "population": district.get("population"),
            "population_density": district.get("population_density"),
            "urban_rate": district.get("urban_rate")
        })
    
    return {
        "year": data.get("year"),
        "total_population": data.get("total_population"),
        "districts": population_data
    }


@router.get("/statistics/economy")
async def get_economy_statistics():
    """获取经济统计数据"""
    data = load_statistics_data()
    if data is None:
        raise HTTPException(status_code=404, detail="统计数据未找到")
    
    economy_data = []
    for district in data.get("districts", []):
        economy_data.append({
            "name": district.get("name"),
            "gdp": district.get("gdp"),
            "gdp_per_capita": district.get("gdp_per_capita"),
            "primary_industry": district.get("primary_industry"),
            "secondary_industry": district.get("secondary_industry"),
            "tertiary_industry": district.get("tertiary_industry")
        })
    
    return {
        "year": data.get("year"),
        "total_gdp": data.get("total_gdp"),
        "districts": economy_data
    }


@router.get("/statistics/resources")
async def get_resource_statistics():
    """获取公共资源统计数据（医疗、教育）"""
    data = load_statistics_data()
    if data is None:
        raise HTTPException(status_code=404, detail="统计数据未找到")
    
    resource_data = []
    for district in data.get("districts", []):
        resource_data.append({
            "name": district.get("name"),
            "hospitals": district.get("hospitals"),
            "hospital_beds": district.get("hospital_beds"),
            "beds_per_1000": district.get("beds_per_1000"),
            "schools": district.get("schools"),
            "teachers": district.get("teachers"),
            "students": district.get("students")
        })
    
    return {"year": data.get("year"), "districts": resource_data}


@router.get("/statistics/{district_name}")
async def get_district_statistics(district_name: str):
    """获取特定区县的统计数据"""
    data = load_statistics_data()
    if data is None:
        raise HTTPException(status_code=404, detail="统计数据未找到")
    
    for district in data.get("districts", []):
        if district.get("name") == district_name or district.get("name", "").startswith(district_name):
            return {"year": data.get("year"), "district": district}
    
    raise HTTPException(status_code=404, detail=f"未找到区县: {district_name}")
