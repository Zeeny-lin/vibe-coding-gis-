"""
FastAPI 应用入口
莆田市市情WebGIS系统后端服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import districts, poi, statistics, analysis, ai, environment, transport, yearbook, economy

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="莆田市市情WebGIS原型系统API服务，融入妈祖文化特色，集成AI智能分析功能。",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(districts.router, prefix=settings.API_PREFIX, tags=["行政区划"])
app.include_router(poi.router, prefix=settings.API_PREFIX, tags=["POI兴趣点"])
app.include_router(statistics.router, prefix=settings.API_PREFIX, tags=["统计数据"])
app.include_router(analysis.router, prefix=settings.API_PREFIX, tags=["空间分析"])
app.include_router(ai.router, prefix=settings.API_PREFIX, tags=["AI助手"])
app.include_router(environment.router, prefix=settings.API_PREFIX, tags=["生态环境"])
app.include_router(transport.router, prefix=settings.API_PREFIX, tags=["交通概况"])
app.include_router(yearbook.router, prefix=settings.API_PREFIX, tags=["统计年鉴"])
app.include_router(economy.router, prefix=f"{settings.API_PREFIX}/economy", tags=["经济产业"])


@app.get("/", tags=["健康检查"])
async def root():
    """API根路径，返回服务状态"""
    return {
        "message": "欢迎使用莆田市市情WebGIS系统API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
