"""
配置管理模块
使用 pydantic-settings 管理应用配置
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    APP_NAME: str = "莆田市市情WebGIS系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API配置
    API_PREFIX: str = "/api/v1"
    
    # CORS配置
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # DeepSeek AI 配置（硅基流动）
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.siliconflow.cn/v1"
    DEEPSEEK_MODEL: str = "deepseek-ai/DeepSeek-V3"

    # Antigravity AI 代理配置
    ANTIGRAVITY_API_KEY: str = ""
    ANTIGRAVITY_BASE_URL: str = "http://127.0.0.1:8045/v1"
    ANTIGRAVITY_MODEL: str = "gemini-2.5-flash"  # Antigravity代理的默认模型

    # 高德地图 API 配置
    AMAP_API_KEY: str = ""
    
    # 可用模型列表 (按provider分组)
    AVAILABLE_MODELS: list[str] = [
        # Antigravity 代理模型
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "claude-sonnet-4-20250514",
        "gpt-4o",
        # DeepSeek/硅基流动 模型
        "deepseek-ai/DeepSeek-V3",
        "deepseek-ai/DeepSeek-R1",
        "Qwen/Qwen2.5-72B-Instruct",
    ]
    
    # AI提供商选择 (deepseek 或 antigravity)
    AI_PROVIDER: str = "antigravity"
    
    # 数据文件路径
    DATA_DIR: Path = Path(__file__).parent.parent / "data"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
