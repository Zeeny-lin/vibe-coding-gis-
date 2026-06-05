"""
AI助手接口
集成DeepSeek大模型，提供智能问答和分析解读功能
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.ai_service import AIService
from app.core.config import settings

router = APIRouter()
ai_service = AIService()


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str  # "user" 或 "assistant"
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    model: Optional[str] = None  # 可选的模型选择
    history: Optional[List[ChatMessage]] = None
    context: Optional[dict] = None  # GIS分析上下文数据


class AnalysisInterpretRequest(BaseModel):
    """分析解读请求模型"""
    analysis_type: str  # 分析类型
    data: dict  # 分析结果数据


@router.post("/ai/chat")
async def chat(request: ChatRequest):
    """
    AI智能问答
    
    与AI助手进行自然语言交互，支持：
    - 莆田市市情问答
    - 妈祖文化介绍
    - GIS功能引导
    - 数据解读
    """
    try:
        response = await ai_service.chat(
            message=request.message,
            history=request.history,
            context=request.context,
            model=request.model
        )
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/interpret")
async def interpret_analysis(request: AnalysisInterpretRequest):
    """
    AI分析解读
    
    对GIS分析结果进行智能解读，生成专业报告
    
    支持的分析类型：
    - accessibility: 可达性分析解读
    - site_selection: 选址建议解读
    - service_coverage: 服务覆盖评估
    - tourism_route: 旅游路线推荐理由
    """
    try:
        interpretation = await ai_service.interpret_analysis(
            analysis_type=request.analysis_type,
            data=request.data
        )
        return {"interpretation": interpretation, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai/suggestions")
async def get_suggestions(topic: str = "general"):
    """
    获取AI建议提示
    
    根据主题返回推荐的问题或操作建议
    """
    suggestions = {
        "general": [
            "介绍一下莆田市的基本情况",
            "莆田市有哪些著名的妈祖庙？",
            "推荐一条妈祖文化旅游路线",
            "分析莆田市医疗资源分布"
        ],
        "tourism": [
            "推荐适合一日游的妈祖文化路线",
            "莆田有哪些必看的景点？",
            "湄洲岛怎么去？有什么特色？",
            "莆田美食有哪些推荐？"
        ],
        "analysis": [
            "分析各区县人口分布情况",
            "评估医疗资源配置均衡性",
            "推荐开设文创商店的最佳位置",
            "对比各区县经济发展水平"
        ]
    }
    
    return {"topic": topic, "suggestions": suggestions.get(topic, suggestions["general"])}


@router.get("/ai/status")
async def ai_status():
    """检查AI服务状态"""
    status = ai_service.check_status()
    return status


@router.get("/ai/models")
async def get_available_models():
    """
    获取可用的AI模型列表
    """
    return {
        "models": settings.AVAILABLE_MODELS,
        "current": settings.DEEPSEEK_MODEL,
        "provider": settings.AI_PROVIDER if hasattr(settings, 'AI_PROVIDER') else "deepseek"
    }


class TourismRecommendRequest(BaseModel):
    """旅游推荐请求模型"""
    preferences: Optional[dict] = None  # 用户偏好：duration(天数), style(休闲/文化/自然), model(模型名称)
    location: Optional[List[float]] = None  # 当前位置 [lng, lat]


class TourismRouteRequest(BaseModel):
    """AI路线规划请求模型"""
    spots: List[str]  # 景点名称列表
    preferences: Optional[dict] = None  # 偏好：mode(driving/walking), optimize(time/distance)


@router.post("/ai/tourism/recommend-spots")
async def recommend_tourism_spots(request: TourismRecommendRequest):
    """
    AI景点推荐
    
    根据用户偏好智能推荐莆田市旅游景点
    返回景点列表（含坐标）用于地图展示
    """
    try:
        duration = request.preferences.get('duration', 1) if request.preferences else 1
        style = request.preferences.get('style', '文化') if request.preferences else '文化'
        model = request.preferences.get('model', None) if request.preferences else None
        
        prompt = f"""请根据以下条件推荐莆田市的旅游景点：
- 游玩天数：{duration}天
- 旅游风格：{style}

请以JSON格式返回推荐景点，格式如下：
{{
    "spots": [
        {{
            "name": "景点名称",
            "coords": [经度, 纬度],
            "description": "简要描述",
            "duration": 建议游览时间(分钟),
            "type": "景点类型"
        }}
    ],
    "summary": "推荐理由总结"
}}

注意：必须包含真实的景点坐标，以便在地图上展示。"""
        
        response = await ai_service.chat(message=prompt, model=model)
        
        # 尝试解析JSON响应
        import json
        import re
        
        # 提取JSON部分
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return {"status": "success", "data": result, "raw_response": response}
            except json.JSONDecodeError:
                pass
        
        return {"status": "success", "raw_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/tourism/plan-route")
async def plan_tourism_route(request: TourismRouteRequest):
    """
    AI路线规划
    
    根据选定景点智能规划最优游览路线
    """
    try:
        spots_str = "、".join(request.spots)
        mode = request.preferences.get('mode', 'driving') if request.preferences else 'driving'
        
        prompt = f"""请为以下景点规划最优游览路线：
景点：{spots_str}
交通方式：{'自驾' if mode == 'driving' else '步行'}

请以JSON格式返回规划结果：
{{
    "route_order": ["景点1", "景点2", ...],
    "total_duration": 预计总时长(分钟),
    "suggestions": [
        "建议1",
        "建议2"
    ],
    "route_reason": "这个游览顺序的理由"
}}"""
        
        response = await ai_service.chat(message=prompt)
        
        import json
        import re
        
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return {"status": "success", "data": result, "raw_response": response}
            except json.JSONDecodeError:
                pass
        
        return {"status": "success", "raw_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
