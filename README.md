# 莆田市市情 WebGIS 系统

## 项目背景

本系统是面向福建省莆田市的 **Web GIS 原型平台**，旨在通过可视化的方式展示城市的 **人口、经济、文化旅游、公共服务** 等多维度数据。项目融合了 **妈祖文化** 的视觉设计元素，并集成了 **AI 智能分析** 能力，为用户提供交互式的数据查询、空间分析与智能问答。

---

## 核心特色

- **妈祖文化主题**：红金配色、传统纹样、文化图标，营造独特的地方品牌形象。  
- **交互式地图**：基于 **Leaflet** 实现的全景地图，支持 POI 标注、图层切换、空间分析。  
- **AI 智能助手**：集成 **DeepSeek** 大模型，提供自然语言问答、旅游路线推荐、数据解读。  
- **多维数据可视化**：使用 **ECharts** 展示人口密度、GDP 结构、公共设施分布等统计图表。  
- **玻璃拟态 UI**：全局使用 CSS 玻璃拟态、渐变、微动画，提升视觉体验。  
- **响应式布局**：在桌面、平板、手机端均保持良好可用性。

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite | 组件化、快速热更新 |
| 前端 UI | Element Plus | 丰富的 UI 组件 |
| 地图 | Leaflet | 开源轻量 GIS 引擎 |
| 图表 | ECharts | 交互式数据可视化 |
| 后端 | Python 3.11 + FastAPI | 高性能异步 API |
| 数据处理 | GeoPandas、Pandas | 空间与表格数据处理 |
| AI 集成 | DeepSeek (OpenAI SDK) | 大模型问答与分析 |
| 部署 | Node.js、uvicorn、Docker（可选） | 本地开发与容器化部署 |

---

## 系统架构

```
+-------------------+        +-------------------+
|   前端 (Vue)      |  <---> |   后端 (FastAPI)  |
| - 页面视图        |        | - RESTful API    |
| - 交互逻辑        |        | - GIS 服务       |
| - AI 调用         |        | - 数据处理       |
+-------------------+        +-------------------+
        |                               |
        |   HTTP/HTTPS (JSON)           |
        v                               v
+-------------------+        +-------------------+
|   静态资源 (CDN) |        |   数据存储 (GeoJSON, |
| - 图片、图标      |        |   CSV, JSON)      |
+-------------------+        +-------------------+
```

- 前端通过 **Axios** 调用后端 API，获取空间数据（GeoJSON）和统计数据（JSON）。
- 后端使用 **GeoPandas** 对矢量数据进行空间分析（如可达性、路径规划），并将结果返回前端。
- AI 助手通过 **DeepSeek SDK** 调用模型，后端包装为统一的 `/ai/chat` 接口供前端使用。

---

## 目录结构

```
putian-gis/
├── backend/                     # 后端代码
│   ├── app/
│   │   ├── api/                # API 路由
│   │   │   ├── gis.py          # GIS 相关接口
│   │   │   ├── ai.py           # AI 接口
│   │   │   └── ...
│   │   ├── core/               # 配置、依赖注入
│   │   ├── services/           # 业务逻辑层
│   │   └── data/               # 静态数据 (GeoJSON, CSV)
│   ├── main.py                 # FastAPI 入口
│   └── requirements.txt        # Python 依赖
├── frontend/                    # 前端代码
│   ├── src/
│   │   ├── assets/             # 图片、图标、地图纹理
│   │   ├── components/         # 通用 UI 组件
│   │   ├── views/              # 页面视图 (Home, Tourism, Meizhou, …)
│   │   ├── router/             # Vue Router 配置
│   │   ├── services/           # Axios API 封装
│   │   └── assets/styles/      # 全局 CSS (玻璃拟态、变量)
│   ├── index.html
│   └── package.json
├── .env                         # 环境变量（AI Key 等）
├── README.md                    # 项目说明文档（本文件）
└── 一键启动.bat                # Windows 启动脚本
```

---

## 功能模块

| 模块 | 关键页面 | 主要功能 |
|------|----------|----------|
| 首页概览 | `HomeView.vue` | 城市概览地图、关键指标卡片、快速入口 |
| 人口分布 | `PopulationView.vue` | 区县人口密度热力图、人口结构图表 |
| 经济产业 | `EconomyView.vue` | GDP 饼图、产业结构柱状图、地区对比 |
| 文化旅游 | `TourismView.vue` / `MeizhouView.vue` | 景点卡片、文化介绍、AI 旅游建议 |
| 公共服务 | `ServiceView.vue` | 医疗、教育资源分布、可达性分析 |
| 交通概况 | `TransportView.vue` | 交通网络图、线路查询、AI 交通解读 |
| 数据年鉴 | `YearbookView.vue` | 历史统计数据、趋势分析 |

---

## 关键实现细节

### 前端
- **组件化**：每个功能模块抽象为独立的 Vue 组件，使用 **Composition API** 管理状态。
- **地图层**：`leaflet` 与 **Vue‑Leaflet** 包装，实现 POI 标注、图层切换、弹窗信息卡。
- **AI 对话**：`AIAssistant.vue` 组件负责 UI，内部通过 `services/ai.js` 调用后端 `/ai/chat` 接口，支持流式返回。
- **全局样式**：`assets/styles/main.css` 使用 CSS 变量实现 **玻璃拟态**（`backdrop-filter: blur(12px)`），并通过 `overflow-y: auto` 解决页面滚动问题。
- **微动画**：使用 `transition` 与 `keyframes` 为卡片、按钮、滚动条添加淡入、漂浮等动画。

### 后端
- **FastAPI**：基于 **async** 实现高并发，自动生成 OpenAPI 文档。
- **GIS 服务**：`app/api/gis.py` 中使用 **GeoPandas** 加载 GeoJSON，提供空间查询（点在多边形内、缓冲区分析）和路径规划（Dijkstra）接口。
- **AI 集成**：`app/api/ai.py` 包装 DeepSeek SDK，统一返回 `{role, content}`，并在异常时返回默认答案，保证前端不崩溃。
- **缓存**：对计算量大的空间分析结果使用 **LRU Cache**（`functools.lru_cache`）进行本地缓存，提升响应速度。
- **配置**：`.env` 中管理 `DEEPSEEK_API_KEY`、`CORS_ORIGINS` 等，使用 **python‑dotenv** 自动加载。

### 数据处理
- **数据来源**：项目自带 `backend/app/data/` 包含行政区划 GeoJSON、POI CSV、统计年鉴 JSON。
- **预处理脚本**：`backend/scripts/preprocess.py` 将原始 Excel/CSV 转换为统一的 GeoJSON/JSON，供 API 直接读取。
- **可视化**：前端通过 `axios` 拉取处理好的 JSON，使用 **ECharts** 渲染柱状、饼图、热力图。

---

## 亮点与创新

1. **文化主题 UI**：深度融合妈祖文化元素（红金配色、纹样、图标），形成独特的地方品牌形象。  
2. **AI 驱动的旅游助手**：基于大模型的自然语言交互，能够根据用户兴趣即时生成旅游路线、景点介绍。  
3. **玻璃拟态 + 微动画**：使用 `backdrop-filter` 与细腻的动画提升现代感，兼顾性能。  
4. **空间分析即服务**：后端提供可达性、最近设施查询、路径规划等 GIS 功能，前端即插即用。  
5. **全栈统一技术**：前端 Vue 3 + Vite、后端 FastAPI，均采用 **异步** 编程模型，开发体验一致。

---

## 安装与快速启动

### 前置条件
- **Node.js** >= 18（推荐 LTS）
- **Python** >= 3.10
- **Git**（可选）

### 步骤
1. **克隆仓库**（如果已有则跳过）
   ```bash
   git clone https://github.com/your-repo/putian-gis.git
   cd putian-gis/putian-gis
   ```
2. **后端环境**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
   - 创建 `.env` 并填入 AI Key（可选）
   ```env
   DEEPSEEK_API_KEY=your_key_here
   ```
3. **启动后端**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. **前端环境**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
5. **访问系统**
   - 前端: http://localhost:5173
   - 后端 API 文档: http://localhost:8000/docs

### 一键启动（Windows）
双击 `一键启动.bat`，脚本会自动启动后端、前端并打开浏览器。

---

## 配置说明

- **`.env`**（后端根目录）
  ```env
  DEEPSEEK_API_KEY=your_api_key   # DeepSeek 大模型密钥，若不填则使用本地模拟
  CORS_ORIGINS=http://localhost:5173
  ```
- **前端 `vite.config.js`** 已预配置代理，将 `/api` 请求转发至 `http://127.0.0.1:8000`。

---

## 贡献指南

1. **Fork** 本仓库并 **clone** 到本地。
2. 创建特性分支 `git checkout -b feature/xxx`。
3. 完成代码、添加单元测试（后端使用 `pytest`，前端使用 `vitest`）。
4. 提交并发起 **Pull Request**，描述变更内容。
5. 通过 CI（GitHub Actions）后合并。

---

## 许可证

本项目采用 **MIT License**，详见 `LICENSE` 文件。

---

## 致谢

- **Element Plus**、**Leaflet**、**ECharts** 开源社区
- **DeepSeek** 提供的 AI 大模型服务
- 项目所有贡献者与使用者

---

*让数据讲述城市故事，让 AI 为旅行保驾护航*
