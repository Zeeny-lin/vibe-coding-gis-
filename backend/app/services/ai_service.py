"""
AI服务
集成DeepSeek大模型，提供智能问答和分析解读功能
"""
from typing import List, Optional, Dict, Any
from openai import OpenAI
from app.core.config import settings


class AIService:
    """AI服务类 - 支持DeepSeek和Antigravity多个AI提供商"""
    
    def __init__(self):
        self.client = None
        self.is_configured = False
        self.provider = settings.AI_PROVIDER if hasattr(settings, 'AI_PROVIDER') else "deepseek"
        self.current_model = None
        
        # 根据配置选择AI提供商
        if self.provider == "antigravity" and settings.ANTIGRAVITY_API_KEY:
            self.client = OpenAI(
                api_key=settings.ANTIGRAVITY_API_KEY,
                base_url=settings.ANTIGRAVITY_BASE_URL
            )
            self.is_configured = True
            self.current_model = settings.ANTIGRAVITY_MODEL
        elif settings.DEEPSEEK_API_KEY:
            self.client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )
            self.is_configured = True
            self.current_model = settings.DEEPSEEK_MODEL
        
        # 系统提示词 - 增强旅游推荐能力
        self.system_prompt = """你是一个专业的城市规划师和GIS专家，专注于福建省莆田市的发展研究。
你熟悉莆田市的地理、人口、经济、文化等各方面情况，尤其对妈祖文化有深入了解。

莆田市基本情况：
- 位置：福建省沿海中部
- 面积：约4200平方公里
- 人口：约320万（2022年）
- 下辖：城厢区、涵江区、荔城区、秀屿区、仙游县（4区1县）
- 特色：妈祖文化发源地，湄洲岛是妈祖祖庙所在地

主要景点及坐标：
1. 湄洲妈祖祖庙 - [119.145120, 25.090959] - 5A级景区，全球妈祖信仰中心
2. 九鲤湖风景区 - [118.821591, 25.460157] - 4A级景区，以湖、洞、瀑、石四奇著称
3. 南少林寺 - [119.041044, 25.539635] - 4A级景区，中国南拳发源地
4. 广化寺 - [118.988960, 25.425153] - 千年古刹，福建佛教四大丛林之一
5. 天妃故里 - [119.138056, 25.089201] - 妈祖林默娘出生地
6. 妈祖文化园 - [119.146000, 25.092000] - 综合性文化旅游区
7. 妈祖影视城 - [119.130928, 25.043880] - 影视文化体验
8. 湄洲岛黄金沙滩 - [119.103421, 25.046464] - 海滩休闲

你的职责：
1. 解答关于莆田市市情的问题
2. 推荐旅游景点和规划旅游路线
3. 解读GIS空间分析结果
4. 提供城市规划和发展建议

当推荐景点或规划路线时，请务必返回景点的坐标信息（格式为 [经度, 纬度]），以便在地图上展示。
请用专业但通俗易懂的语言回答问题。"""

    def check_status(self) -> Dict:
        """检查AI服务状态"""
        return {
            "configured": self.is_configured,
            "provider": self.provider,
            "model": self.current_model if self.is_configured else None,
            "status": "ready" if self.is_configured else "not_configured",
            "message": f"AI服务已就绪 (Provider: {self.provider})" if self.is_configured else "请配置AI API密钥"
        }
    
    async def chat(self, message: str, history: Optional[List] = None, 
                   context: Optional[Dict] = None, model: Optional[str] = None) -> str:
        """
        AI聊天
        """
        if not self.is_configured:
            return self._mock_response(message)
        
        # 使用指定模型或当前配置的模型
        use_model = model or self.current_model
        
        # 构建消息列表
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # 添加历史消息
        if history:
            for msg in history:
                messages.append({
                    "role": msg.role if hasattr(msg, 'role') else msg.get("role"),
                    "content": msg.content if hasattr(msg, 'content') else msg.get("content")
                })
        
        # 添加上下文
        if context:
            context_str = f"\n\n当前GIS分析上下文数据：\n{context}"
            messages.append({"role": "system", "content": context_str})
        
        # 添加用户消息
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=use_model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI服务调用失败: {str(e)}"
    
    async def interpret_analysis(self, analysis_type: str, data: Dict) -> str:
        """
        分析结果解读
        """
        if not self.is_configured:
            return self._mock_interpretation(analysis_type, data)
        
        prompts = {
            "accessibility": f"""请分析以下可达性分析结果，评估公共服务覆盖的均衡性：
{data}

请从以下角度进行解读：
1. 各区县的可达性差异
2. 服务覆盖的薄弱区域
3. 改善建议""",
            
            "site_selection": f"""请解读以下选址分析结果，给出专业建议：
{data}

请说明：
1. 推荐位置的优势
2. 潜在风险
3. 经营建议""",
            
            "service_coverage": f"""请评估以下公共服务覆盖分析结果：
{data}

请分析：
1. 当前覆盖水平
2. 服务盲区识别
3. 优化建议""",
            
            "tourism_route": f"""请为以下旅游路线提供推荐理由和旅行建议：
{data}

请包含：
1. 路线亮点
2. 游览建议
3. 注意事项"""
        }
        
        prompt = prompts.get(analysis_type, f"请解读以下分析结果：\n{data}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"分析解读失败: {str(e)}"
    
    def _mock_response(self, message: str) -> str:
        """模拟响应（未配置API时使用）"""
        responses = {
            "介绍": """莆田市位于福建省沿海中部，是著名的妈祖文化发源地。

**基本情况：**
- 总面积：约4200平方公里
- 常住人口：约320万人
- 行政区划：城厢区、涵江区、荔城区、秀屿区、仙游县

**特色亮点：**
1. **妈祖文化**：湄洲岛是妈祖祖庙所在地，每年吸引大量海内外信众朝圣
2. **工艺美术**：木雕、石雕、玉雕等传统工艺闻名全国
3. **特色美食**：卤面、兴化粉、海蛎饼等地方特色

如需了解更多详情，请配置AI服务或选择具体功能模块。""",
            
            "妈祖": """**妈祖文化简介**

妈祖，原名林默，是福建莆田湄洲岛人，生于宋建隆元年（960年）。她一生扶危济困、救助海难，深受沿海民众敬仰。

**主要景点：**
1. **湄洲妈祖祖庙** - 全球妈祖信仰中心
2. **天妃故里** - 妈祖出生地
3. **妈祖文化园** - 综合性文化旅游区

**推荐路线：**
湄洲岛一日游：祖庙→天妃故里→妈祖文化园→黄金沙滩

建议游览时间：1-2天""",
            
            "旅游": """**莆田旅游推荐**

🏛️ **人文景观**
- 湄洲妈祖祖庙（5A级景区）
- 南少林寺
- 广化寺

🌊 **自然风光**
- 九鲤湖风景区
- 湄洲岛沙滩
- 莆田二十四景

🍜 **美食推荐**
- 莆田卤面
- 兴化粉
- 海蛎饼
- 套肠

📅 **最佳旅游时间**：春秋两季"""
        }
        
        # 简单关键词匹配
        for key, response in responses.items():
            if key in message:
                return response
        
        return """感谢您的问题！

目前AI服务尚未配置，无法提供智能回复。请按以下步骤配置：

1. 获取DeepSeek API密钥
2. 在后端目录创建 `.env` 文件
3. 添加配置：`DEEPSEEK_API_KEY=your-api-key`
4. 重启服务

您也可以通过系统的各功能模块探索莆田市市情数据。"""
    
    def _mock_interpretation(self, analysis_type: str, data: Dict) -> str:
        """模拟分析解读（未配置API时使用）"""
        interpretations = {
            "accessibility": """**可达性分析解读**

根据分析结果，莆田市各区县的公共服务可达性存在一定差异：

1. **城厢区、荔城区**：作为主城区，设施密度较高，可达性较好
2. **涵江区**：发展较快，服务设施正在完善中
3. **秀屿区、仙游县**：相对偏远，部分区域存在服务盲区

**建议：**
- 加强农村地区医疗卫生站点布局
- 优化校车路线，提升教育可达性""",
            
            "site_selection": """**选址建议解读**

根据加权叠加分析，推荐区域具有以下优势：

1. **人口密度适中**：确保客源充足
2. **交通便利**：便于顾客到达
3. **竞争适度**：避免过度竞争

**经营建议：**
- 结合当地文化特色
- 注重服务质量
- 建立品牌形象""",
            
            "tourism_route": """**旅游路线推荐理由**

这条路线精心规划，具有以下特点：

1. **文化深度**：深入体验妈祖信仰
2. **景点衔接**：优化游览顺序
3. **时间合理**：充裕且不疲劳

**游览建议：**
- 提前预订船票（前往湄洲岛）
- 穿着舒适鞋子
- 带好防晒用品"""
        }
        
        return interpretations.get(analysis_type, "分析解读功能需要配置AI服务，请设置DEEPSEEK_API_KEY。")
