"""
统计年鉴数据接口
提供莆田市历史统计年鉴数据
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from app.core.config import settings

router = APIRouter()


def load_yearbook_data():
    """加载年鉴数据"""
    data_file = settings.DATA_DIR / "yearbook.json"
    if not data_file.exists():
        return None
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/yearbook")
async def get_yearbook_summary():
    """
    获取统计年鉴汇总数据
    
    返回近10年的主要经济社会指标
    """
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return data


@router.get("/yearbook/gdp")
async def get_gdp_data():
    """获取GDP历史数据"""
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return {
        "years": data["years"],
        "gdp": data["gdp"],
        "gdpGrowth": data["gdpGrowth"],
        "perCapitaGDP": data["perCapitaGDP"]
    }


@router.get("/yearbook/population")
async def get_population_data():
    """获取人口历史数据"""
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return {
        "years": data["years"],
        "population": data["population"],
        "urbanPopulationRate": data["urbanPopulationRate"]
    }


@router.get("/yearbook/income")
async def get_income_data():
    """获取居民收入历史数据"""
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return {
        "years": data["years"],
        "urbanIncome": data["urbanIncome"],
        "ruralIncome": data["ruralIncome"]
    }


@router.get("/yearbook/industry")
async def get_industry_data():
    """获取产业结构数据"""
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return {
        "years": data["years"],
        "industrialOutput": data["industrialOutput"],
        "retailSales": data["retailSales"],
        "industryStructure": data["industryStructure"]
    }


@router.get("/yearbook/districts")
async def get_district_gdp():
    """获取各区县GDP数据"""
    data = load_yearbook_data()
    if data is None:
        raise HTTPException(status_code=404, detail="年鉴数据未找到")
    return data.get("districtGDP2023", {})
