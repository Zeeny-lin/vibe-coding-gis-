<template>
  <div class="tourism-view">
    <!-- 地图区域 -->
    <div class="map-section">
      <div class="api-notice">
        <el-alert
          title="地图交互说明"
          type="success"
          show-icon
          :closable="true"
          description="点击地图可获取坐标信息，AI推荐的景点会在地图上以标记显示。"
        />
      </div>
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="tourismPOI"
        :showLayerControl="false"
        @mapReady="onMapReady"
      />

      <!-- 路线显示 -->
      <div class="route-display" v-if="routeData">
        <div class="route-info panel">
          <h4>🛤️ {{ routeData.route_name }}</h4>
          <p>{{ routeData.description }}</p>
          <div class="route-stats">
            <span><strong>{{ routeData.total_distance }}</strong> 公里</span>
            <span><strong>{{ routeData.spots?.length }}</strong> 个景点</span>
            <span><strong>{{ Math.floor(routeData.total_duration / 60) }}</strong> 小时</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧面板 -->
    <div class="tourism-panel">
      <div class="panel-header">
        <span class="panel-title">🌊 妈祖文化旅游</span>
      </div>

      <!-- 走进湄洲岛入口 (新增) -->
      <div class="meizhou-entry" @click="goToMeizhou">
        <div class="entry-content">
          <h3>🏝️ 走进湄洲岛</h3>
          <p>探索妈祖故里，开启圣地之旅</p>
        </div>
        <div class="entry-icon">➜</div>
      </div>

      <!-- 路线选择 -->
      <div class="route-selector">
        <h4>选择旅游路线</h4>
        <el-radio-group v-model="selectedDuration" @change="loadRoute">
          <el-radio-button :value="1">一日游</el-radio-button>
          <el-radio-button :value="2">两日游</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 景点列表 -->
      <div class="spots-section" v-if="routeData?.spots">
        <h4>游览景点</h4>
        <div class="spots-timeline">
          <div 
            class="spot-item" 
            v-for="(spot, index) in routeData.spots" 
            :key="index"
          >
            <div class="spot-marker">
              <span class="marker-number">{{ index + 1 }}</span>
              <div class="marker-line" v-if="index < routeData.spots.length - 1"></div>
            </div>
            <div class="spot-content">
              <h5>{{ spot.name }}</h5>
              <p>{{ spot.description }}</p>
              <span class="spot-duration">⏱️ 建议游览 {{ spot.duration }} 分钟</span>
            </div>
          </div>
        </div>
      </div>

      <!-- AI解读 -->
      <div class="ai-interpretation" v-if="aiInterpretation">
        <h4>✨ AI旅行建议</h4>
        <div class="interpretation-content" v-html="formatMarkdown(aiInterpretation)"></div>
      </div>

      <!-- AI智能推荐 -->
      <div class="ai-recommend-section">
        <h4>🤖 AI智能助手</h4>
        <div class="ai-recommend-options">
          <el-select v-model="aiTourStyle" placeholder="旅游风格" size="small" style="margin-bottom: 8px;">
            <el-option label="文化体验" value="文化" />
            <el-option label="自然风光" value="自然" />
            <el-option label="休闲度假" value="休闲" />
            <el-option label="深度游览" value="深度" />
          </el-select>
          <el-select v-model="aiModel" placeholder="选择AI模型" size="small">
            <el-option label="Gemini 2.5 Flash (推荐)" value="gemini-2.5-flash" />
            <el-option label="Gemini 2.5 Pro" value="gemini-2.5-pro" />
            <el-option label="Claude Sonnet 4" value="claude-sonnet-4-20250514" />
            <el-option label="GPT-4o" value="gpt-4o" />
            <el-option label="DeepSeek V3" value="deepseek-ai/DeepSeek-V3" />
          </el-select>
        </div>
        <div class="ai-recommend-buttons">
          <el-button 
            type="primary" 
            class="ai-btn"
            @click="getAISpotRecommendation"
            :loading="aiSpotLoading"
          >
            <el-icon><MagicStick /></el-icon>
            AI推荐景点
          </el-button>
          <el-button 
            type="info" 
            @click="getAIRecommendation"
            :loading="aiLoading"
          >
            获取行程建议
          </el-button>
        </div>
      </div>

      <!-- AI推荐的景点展示 + DIY路线规划 -->
      <div class="diy-route-section" v-if="aiRecommendedSpots.length > 0 || routeSpots.length > 0">
        <h4>🛤️ DIY路线规划</h4>
        
        <!-- 出行方式选择 -->
        <div class="travel-mode-selector">
          <span class="mode-label">出行方式：</span>
          <el-radio-group v-model="travelMode" size="small" @change="replanRoute">
            <el-radio-button label="driving">🚗 驾车</el-radio-button>
            <el-radio-button label="walking">🚶 步行</el-radio-button>
            <el-radio-button label="cycling">🚴 骑行</el-radio-button>
            <el-radio-button label="transit">🚌 公交</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 已选择的路线景点 -->
        <div class="route-spots-list">
          <div 
            class="route-spot-item" 
            v-for="(spot, index) in routeSpots" 
            :key="spot.name + index"
            draggable="true"
          >
            <span class="route-spot-index">{{ index + 1 }}</span>
            <div class="route-spot-info" @click="focusAISpot(spot)">
              <span class="route-spot-name">{{ spot.name }}</span>
              <span class="route-spot-duration">⏱️ {{ spot.duration || 60 }}分钟</span>
            </div>
            <el-button 
              size="small" 
              type="danger" 
              circle 
              @click.stop="removeFromRoute(index)"
            >
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          
          <div v-if="routeSpots.length === 0" class="empty-route-hint">
            点击下方AI推荐的景点「加入路线」开始规划
          </div>
        </div>

        <!-- 快捷操作 -->
        <div class="route-actions">
          <el-button 
            type="primary" 
            @click="replanRoute" 
            :loading="routePlanLoading"
            :disabled="routeSpots.length < 2"
          >
            📍 重新规划路线
          </el-button>
          <el-button 
            type="warning" 
            @click="clearRoute"
            :disabled="routeSpots.length === 0"
          >
            清空路线
          </el-button>
        </div>

        <!-- 路线信息 -->
        <div class="route-result-info" v-if="routeInfo">
          <div class="info-row">
            <span>📏 总里程：{{ routeInfo.distance }}</span>
            <span>⏱️ 预计时间：{{ routeInfo.duration }}</span>
          </div>
          <div class="info-row">
            <span>🚗 出行方式：{{ routeInfo.modeName }}</span>
          </div>
        </div>
        
        <el-divider />
        
        <!-- AI推荐景点（可加入路线） -->
        <h5 style="margin: 0 0 8px; color: var(--text-secondary);">✨ 可添加的景点</h5>
        <div class="ai-spots-list">
          <div 
            class="ai-spot-item" 
            v-for="(spot, index) in aiRecommendedSpots" 
            :key="'ai-' + index"
            @click="focusAISpot(spot)"
          >
            <span class="ai-spot-index">{{ index + 1 }}</span>
            <div class="ai-spot-info">
              <span class="ai-spot-name">{{ spot.name }}</span>
              <span class="ai-spot-desc">{{ spot.description }}</span>
            </div>
            <el-button 
              size="small" 
              :type="isSpotInRoute(spot) ? 'info' : 'primary'" 
              :disabled="isSpotInRoute(spot)"
              @click.stop="addSpotToRoute(spot)"
            >
              {{ isSpotInRoute(spot) ? '已添加' : '加入' }}
            </el-button>
          </div>
        </div>
      </div>

      <!-- 操作按钮组 -->
      <div class="action-buttons">
        <el-button 
          type="success"
          @click="showRouteOnMap"
          :disabled="!routeData"
        >
          📍 地图显示路线
        </el-button>
        <el-button 
          type="warning"
          @click="exportTravelPlan"
          :disabled="!routeData"
        >
          📄 导出旅游计划
        </el-button>
      </div>

      <!-- 景区范围开关 -->
      <div class="layer-toggle">
        <el-checkbox v-model="showScenicAreas" @change="toggleScenicAreas">
          显示景区范围
        </el-checkbox>
      </div>

      <!-- 热门景点 -->
      <div class="hot-spots">
        <h4>🔥 热门景点</h4>
        <div class="spot-cards">
          <div 
            class="spot-card" 
            v-for="spot in hotSpots" 
            :key="spot.id"
            @click="focusSpot(spot)"
          >
            <div class="spot-icon" :style="{ background: spot.color }">
              {{ spot.icon }}
            </div>
            <div class="spot-info">
              <span class="spot-name">{{ spot.name }}</span>
              <span class="spot-type">{{ spot.type }}</span>
            </div>
            <el-button 
              size="small" 
              type="primary" 
              @click.stop="showSpotDetail(spot)"
              class="detail-btn"
            >
              详情
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 景点详情弹窗 -->
    <el-dialog 
      v-model="spotDialogVisible" 
      :title="selectedSpot?.name" 
      width="500px"
      class="spot-dialog"
    >
      <div class="spot-detail" v-if="selectedSpot">
        <div class="detail-header">
          <div class="detail-icon" :style="{ background: selectedSpot.color }">
            {{ selectedSpot.icon }}
          </div>
          <div class="detail-meta">
            <span class="detail-type">{{ selectedSpot.type }}</span>
            <span class="detail-district">📍 {{ selectedSpot.district }}</span>
          </div>
        </div>
        <div class="detail-body">
          <p class="detail-desc">{{ selectedSpot.description }}</p>
          <div class="detail-info-grid">
            <div class="info-item">
              <span class="info-label">🕐 开放时间</span>
              <span class="info-value">{{ selectedSpot.openTime }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">🎫 门票价格</span>
              <span class="info-value">{{ selectedSpot.ticket }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">⏱️ 建议游玩</span>
              <span class="info-value">{{ selectedSpot.suggestTime }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">📞 咨询电话</span>
              <span class="info-value">{{ selectedSpot.phone }}</span>
            </div>
          </div>
        </div>
        <div class="detail-footer">
          <el-button type="primary" @click="focusAndClose(selectedSpot)">
            在地图上查看
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { MagicStick, Close } from '@element-plus/icons-vue'
import { marked } from 'marked'
import L from 'leaflet'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

const router = useRouter()
const mapRef = ref(null)
const districtsData = ref(null)
const tourismPOI = ref(null)
const routeData = ref(null)
const selectedDuration = ref(1)
const aiInterpretation = ref('')
const aiLoading = ref(false)
const showScenicAreas = ref(false)
let scenicAreasLayer = null
let routeLineLayer = null
const spotDialogVisible = ref(false)
const selectedSpot = ref(null)

const goToMeizhou = () => {
  router.push('/meizhou')
}

// AI智能推荐相关
const aiSpotLoading = ref(false)
const aiTourStyle = ref('文化')
const aiModel = ref('gemini-2.5-flash')  // 默认使用Gemini 2.5 Flash
const aiRecommendedSpots = ref([])
let aiSpotMarkersLayer = null
let mapInstance = null

// DIY路线规划相关
const routeSpots = ref([])  // 用户选择的路线景点
const travelMode = ref('driving')  // 出行方式
const routePlanLoading = ref(false)
const routeInfo = ref(null)  // 路线规划结果信息

// 热门景点（增强数据）
const hotSpots = [
  { 
    id: 1, 
    name: '湄洲妈祖祖庙', 
    type: '5A级景区', 
    icon: '🏛️', 
    color: '#C41E3A', 
    coords: [25.090959, 119.145120],
    district: '秀屿区',
    description: '湄洲妈祖祖庙是全球5000多座妈祖庙的祖庙，被誉为"东方麦加"。这里供奉着海上女神妈祖，是两岸文化交流的重要纽带，每年吸引数百万信众朝圣。',
    openTime: '全年 06:00-18:00',
    ticket: '免费',
    suggestTime: '2-3小时',
    phone: '0594-5086688'
  },
  { 
    id: 2, 
    name: '九鲤湖风景区', 
    type: '4A级景区', 
    icon: '🌊', 
    color: '#006994', 
    coords: [25.460157, 118.821591],
    district: '仙游县',
    description: '九鲤湖以湖、洞、瀑、石四奇著称，是福建著名的风景名胜区。相传汉武帝时，有九仙于此炼丹济世，乘鲤升仙，故名九鲤湖。',
    openTime: '全年 08:00-17:30',
    ticket: '成人票 ¥50',
    suggestTime: '3-4小时',
    phone: '0594-8269288'
  },
  { 
    id: 3, 
    name: '南少林寺', 
    type: '4A级景区', 
    icon: '🥋', 
    color: '#FFD700', 
    coords: [25.539635, 119.041044],
    district: '荔城区',
    description: '福建南少林寺是中国南拳的发源地，与河南嵩山少林寺并称南北少林。寺内保存有大量珍贵的少林武术文化遗产。',
    openTime: '全年 07:30-17:30',
    ticket: '成人票 ¥30',
    suggestTime: '1.5-2小时',
    phone: '0594-2533516'
  },
  { 
    id: 4, 
    name: '广化寺', 
    type: '千年古刹', 
    icon: '🏯', 
    color: '#00C853', 
    coords: [25.425153, 118.988960],
    district: '城厢区',
    description: '广化寺创建于南朝陈永定二年（558年），是福建佛教四大丛林之一。寺内建筑宏伟，文物众多，是闽中著名的千年古刹。',
    openTime: '全年 06:00-17:00',
    ticket: '免费',
    suggestTime: '1-2小时',
    phone: '0594-2699553'
  }
]

// 格式化Markdown
const formatMarkdown = (content) => {
  try {
    return marked.parse(content)
  } catch {
    return content
  }
}

// 加载路线
const loadRoute = async () => {
  try {
    const route = await api.tourismRoute('mazu', selectedDuration.value)
    routeData.value = route
    aiInterpretation.value = ''
  } catch (error) {
    console.error('加载路线失败:', error)
    // 使用模拟数据
    routeData.value = {
      route_name: selectedDuration.value === 1 ? '妈祖朝圣一日游' : '妈祖文化深度两日游',
      description: '深度体验妈祖文化的经典路线',
      total_distance: selectedDuration.value === 1 ? 15.5 : 85.2,
      total_duration: selectedDuration.value === 1 ? 330 : 630,
      spots: [
        { name: '湄洲妈祖祖庙', description: '妈祖祖庙，朝圣圣地', duration: 120 },
        { name: '天妃故里', description: '妈祖林默娘出生地', duration: 60 },
        { name: '妈祖文化园', description: '了解妈祖文化', duration: 90 },
        { name: '湄洲岛黄金沙滩', description: '休闲放松', duration: 60 }
      ]
    }
  }
}

// 获取AI旅行建议
const getAIRecommendation = async () => {
  aiLoading.value = true
  try {
    const response = await api.interpretAnalysis('tourism_route', routeData.value)
    aiInterpretation.value = response.interpretation
  } catch (error) {
    aiInterpretation.value = `**旅行建议**

这条${routeData.value.route_name}精心规划，具有以下特点：

1. **文化深度**：深入体验妈祖信仰，感受千年文化传承
2. **景点衔接**：优化游览顺序，减少路途奔波
3. **时间合理**：充裕且不疲劳

**游览建议：**
- 提前预订前往湄洲岛的船票
- 穿着舒适的运动鞋
- 带好防晒用品和相机
- 品尝当地特色美食：卤面、兴化粉`
  } finally {
    aiLoading.value = false
  }
}

// AI智能景点推荐 - 使用本地预设数据（避免API配额问题）
const getAISpotRecommendation = async () => {
  aiSpotLoading.value = true
  
  // 预设的景点数据库（按风格分类）
  const spotDatabase = {
    '文化': [
      { name: '湄洲妈祖祖庙', coords: [119.145120, 25.090959], description: '5A级景区，全球妈祖信仰中心', duration: 120, type: '文化景区' },
      { name: '广化寺', coords: [118.988960, 25.425153], description: '千年古刹，福建四大丛林', duration: 60, type: '宗教文化' },
      { name: '南少林寺', coords: [119.041044, 25.539635], description: '中国南拳发源地', duration: 90, type: '武术文化' },
      { name: '天妃故里', coords: [119.138056, 25.089201], description: '妈祖林默娘出生地', duration: 60, type: '历史遗迹' }
    ],
    '自然': [
      { name: '九鲤湖风景区', coords: [118.821591, 25.460157], description: '4A级景区，九漈飞瀑闻名遐迩', duration: 180, type: '自然风光' },
      { name: '湄洲岛黄金沙滩', coords: [119.103421, 25.046464], description: '细沙金黄，海水清澈', duration: 90, type: '海滨风光' },
      { name: '菜溪岩', coords: [118.753889, 25.570833], description: '奇岩怪石，森林茂密', duration: 120, type: '地质公园' },
      { name: '瑞云山森林公园', coords: [119.000000, 25.550000], description: '天然氧吧，避暑胜地', duration: 90, type: '森林公园' }
    ],
    '休闲': [
      { name: '莆田市图书馆', coords: [119.007813, 25.454861], description: '现代化图书馆，文化休闲好去处', duration: 60, type: '文化设施' },
      { name: '木兰溪湿地公园', coords: [118.997222, 25.438889], description: '城市绿肺，休闲散步', duration: 60, type: '城市公园' },
      { name: '涵江区步行街', coords: [119.116667, 25.458333], description: '购物美食一条街', duration: 90, type: '商业街区' },
      { name: '妈祖文化园', coords: [119.146000, 25.092000], description: '了解妈祖文化的最佳去处', duration: 90, type: '主题公园' }
    ],
    '深度': [
      { name: '湄洲妈祖祖庙', coords: [119.145120, 25.090959], description: '5A级景区，全球妈祖信仰中心', duration: 150, type: '文化景区' },
      { name: '九鲤湖风景区', coords: [118.821591, 25.460157], description: '4A级景区，祈梦文化发源地', duration: 200, type: '自然风光' },
      { name: '南少林寺', coords: [119.041044, 25.539635], description: '深入了解南少林武术文化', duration: 120, type: '武术文化' },
      { name: '广化寺', coords: [118.988960, 25.425153], description: '体验禅修，感悟佛法', duration: 90, type: '宗教文化' },
      { name: '菜溪岩', coords: [118.753889, 25.570833], description: '探索地质奇观', duration: 150, type: '地质公园' }
    ]
  }
  
  // 根据选择的风格获取推荐景点
  const style = aiTourStyle.value || '文化'
  const spots = spotDatabase[style] || spotDatabase['文化']
  
  // 模拟加载延迟
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // 根据天数调整推荐数量
  const spotCount = Math.min(selectedDuration.value * 2 + 2, spots.length)
  aiRecommendedSpots.value = spots.slice(0, spotCount)
  
  // 生成AI建议文字
  const spotNames = aiRecommendedSpots.value.map(s => s.name).join(' → ')
  aiInterpretation.value = `**推荐路线：${spotNames}**

根据您选择的${style}风格和${selectedDuration.value}天行程，为您规划了以上${aiRecommendedSpots.value.length}个景点。

**游玩建议：**
- 按照标记顺序依次游览
- 每个景点预留充足时间
- 注意景区开放时间`
  
  // 在地图上显示并绘制路线
  showAISpotsOnMap()
  
  aiSpotLoading.value = false
}

// 在地图上显示AI推荐的景点 (Leaflet版本)
const showAISpotsOnMap = () => {
  const map = mapInstance || mapRef.value?.getMap()
  if (!map || aiRecommendedSpots.value.length === 0) return
  
  // 清除之前的标记
  if (aiSpotMarkersLayer) {
    map.removeLayer(aiSpotMarkersLayer)
  }
  
  // 创建新的图层组
  aiSpotMarkersLayer = L.layerGroup().addTo(map)
  
  const bounds = []
  aiRecommendedSpots.value.forEach((spot, idx) => {
    if (!spot.coords || spot.coords.length < 2) return
    
    // coords格式: [lng, lat]，Leaflet需要 [lat, lng]
    const latLng = [spot.coords[1], spot.coords[0]]
    bounds.push(latLng)
    
    // 创建自定义图标
    const icon = L.divIcon({
      className: 'ai-spot-marker',
      html: `<div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 14px;
      ">${idx + 1}</div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    })
    
    L.marker(latLng, { icon })
      .bindPopup(`
        <div style="min-width: 200px;">
          <h4 style="margin: 0 0 8px; color: #764ba2;">🤖 ${spot.name}</h4>
          <p style="margin: 0 0 8px; font-size: 13px;">${spot.description || ''}</p>
          ${spot.duration ? `<p style="margin: 0; font-size: 12px; color: #666;">⏱️ 建议游览 ${spot.duration} 分钟</p>` : ''}
        </div>
      `)
      .addTo(aiSpotMarkersLayer)
  })
  
  // 缩放到所有标记的范围
  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [50, 50] })
  }
  
  // 自动生成推荐路线
  drawAIRouteOnMap()
}

// 在地图上绘制AI推荐路线 - 调用高德API获取真实路径
const drawAIRouteOnMap = async () => {
  const map = mapInstance || mapRef.value?.getMap()
  if (!map || aiRecommendedSpots.value.length < 2) return
  
  // 如果已有AI路线层，先移除
  if (window.aiRouteLine) {
    map.removeLayer(window.aiRouteLine)
  }
  
  // 获取所有有效的坐标点
  const validSpots = aiRecommendedSpots.value.filter(spot => spot.coords && spot.coords.length >= 2)
  if (validSpots.length < 2) return
  
  // 起点和终点
  const start = validSpots[0].coords  // [lng, lat]
  const end = validSpots[validSpots.length - 1].coords  // [lng, lat]
  
  // 途经点（中间点）
  const waypoints = validSpots.length > 2 
    ? validSpots.slice(1, -1).map(spot => spot.coords)
    : null
  
  try {
    // 调用后端路线规划API（使用高德地图驾车路线）
    const response = await api.planRoute(start, end, waypoints)
    
    if (response && response.route_path && response.route_path.length > 0) {
      // 将路径转换为Leaflet格式 [lat, lng]
      const pathLatLngs = response.route_path.map(coord => [coord[1], coord[0]])
      
      // 绘制真实导航路线
      window.aiRouteLine = L.polyline(pathLatLngs, {
        color: '#764ba2',
        weight: 5,
        opacity: 0.9,
        lineJoin: 'round'
      }).addTo(map)
      
      // 更新路线信息显示
      const distanceKm = (response.total_distance / 1000).toFixed(1)
      const durationMin = Math.round(response.estimated_time)
      
      aiInterpretation.value += `\n\n**路线信息：**
- 总里程：${distanceKm} 公里
- 预计行车时间：${durationMin} 分钟
- 规划模式：驾车导航`
    } else {
      // API失败时回退到简单连线
      drawSimpleRoute()
    }
  } catch (error) {
    console.error('路线规划失败:', error)
    // 回退到简单连线
    drawSimpleRoute()
  }
}

// 简单连线（API失败时的备用方案）
const drawSimpleRoute = () => {
  const map = mapInstance || mapRef.value?.getMap()
  if (!map || aiRecommendedSpots.value.length < 2) return
  
  const routePoints = aiRecommendedSpots.value
    .filter(spot => spot.coords && spot.coords.length >= 2)
    .map(spot => [spot.coords[1], spot.coords[0]])  // [lat, lng]
  
  if (routePoints.length < 2) return
  
  window.aiRouteLine = L.polyline(routePoints, {
    color: '#764ba2',
    weight: 4,
    opacity: 0.8,
    dashArray: '10, 10'
  }).addTo(map)
}

// 聚焦到AI推荐的景点 (Leaflet版本)
const focusAISpot = (spot) => {
  const map = mapInstance || mapRef.value?.getMap()
  if (!map || !spot.coords) return
  
  // coords格式: [lng, lat]，Leaflet需要 [lat, lng]
  const latLng = [spot.coords[1], spot.coords[0]]
  map.flyTo(latLng, 15, { duration: 1.5 })
}

// 将AI推荐的景点添加到DIY路线
const addSpotToRoute = (spot) => {
  const exists = routeSpots.value.find(s => s.name === spot.name)
  if (!exists) {
    routeSpots.value.push({
      name: spot.name,
      coords: spot.coords,
      description: spot.description,
      duration: spot.duration || 60
    })
    // 自动重新规划路线
    if (routeSpots.value.length >= 2) {
      replanRoute()
    }
  }
}

// 检查景点是否已在路线中
const isSpotInRoute = (spot) => {
  return routeSpots.value.some(s => s.name === spot.name)
}

// 从路线中移除景点
const removeFromRoute = (index) => {
  routeSpots.value.splice(index, 1)
  // 自动重新规划路线
  if (routeSpots.value.length >= 2) {
    replanRoute()
  } else {
    // 清除地图上的路线
    const map = mapInstance || mapRef.value?.getMap()
    if (map && window.aiRouteLine) {
      map.removeLayer(window.aiRouteLine)
      window.aiRouteLine = null
    }
    routeInfo.value = null
  }
}

// 清空路线
const clearRoute = () => {
  routeSpots.value = []
  routeInfo.value = null
  // 清除地图上的路线
  const map = mapInstance || mapRef.value?.getMap()
  if (map && window.aiRouteLine) {
    map.removeLayer(window.aiRouteLine)
    window.aiRouteLine = null
  }
}

// 重新规划路线
const replanRoute = async () => {
  if (routeSpots.value.length < 2) return
  
  routePlanLoading.value = true
  const map = mapInstance || mapRef.value?.getMap()
  
  // 清除之前的路线
  if (map && window.aiRouteLine) {
    map.removeLayer(window.aiRouteLine)
  }
  
  // 获取起终点和途经点
  const validSpots = routeSpots.value.filter(spot => spot.coords && spot.coords.length >= 2)
  if (validSpots.length < 2) {
    routePlanLoading.value = false
    return
  }
  
  const start = validSpots[0].coords
  const end = validSpots[validSpots.length - 1].coords
  const waypoints = validSpots.length > 2 
    ? validSpots.slice(1, -1).map(spot => spot.coords)
    : null
  
  try {
    // 调用后端API，传递出行方式
    const response = await api.planRoute(start, end, waypoints, travelMode.value)
    
    if (response && response.route_path && response.route_path.length > 0) {
      // 绘制路线
      const pathLatLngs = response.route_path.map(coord => [coord[1], coord[0]])
      
      // 根据出行方式选择颜色
      const modeColors = {
        'driving': '#3498db',
        'walking': '#27ae60',
        'cycling': '#f39c12',
        'transit': '#9b59b6'
      }
      
      window.aiRouteLine = L.polyline(pathLatLngs, {
        color: modeColors[travelMode.value] || '#764ba2',
        weight: 5,
        opacity: 0.9,
        lineJoin: 'round'
      }).addTo(map)
      
      // 更新路线信息
      const distanceKm = (response.total_distance / 1000).toFixed(1)
      const durationMin = Math.round(response.estimated_time)
      
      routeInfo.value = {
        distance: `${distanceKm} 公里`,
        duration: `${durationMin} 分钟`,
        modeName: response.mode_name || '驾车'
      }
      
      // 缩放到路线范围
      map.fitBounds(window.aiRouteLine.getBounds(), { padding: [50, 50] })
    }
  } catch (error) {
    console.error('路线规划失败:', error)
    // 回退到简单连线
    const routePoints = validSpots.map(spot => [spot.coords[1], spot.coords[0]])
    window.aiRouteLine = L.polyline(routePoints, {
      color: '#764ba2',
      weight: 4,
      opacity: 0.8,
      dashArray: '10, 10'
    }).addTo(map)
    
    routeInfo.value = {
      distance: '计算失败',
      duration: '-',
      modeName: '直线连接'
    }
  } finally {
    routePlanLoading.value = false
  }
}

// 保留旧方法兼容性
const addToRoute = addSpotToRoute

// 地图就绪回调 - 启用地图交互
const onMapReady = (map) => {
  mapInstance = map
  
  // 启用地图点击事件
  map.on('click', (e) => {
    const { lat, lng } = e.latlng
    console.log('地图点击:', lat, lng)
    
    // 显示点击位置的信息弹窗
    L.popup()
      .setLatLng(e.latlng)
      .setContent(`
        <div style="text-align: center;">
          <p style="margin: 0 0 8px; font-size: 12px;">📍 点击位置</p>
          <p style="margin: 0; font-size: 11px; color: #666;">经度: ${lng.toFixed(6)}<br>纬度: ${lat.toFixed(6)}</p>
        </div>
      `)
      .openOn(map)
  })
}

// 显示景点详情
const showSpotDetail = (spot) => {
  selectedSpot.value = spot
  spotDialogVisible.value = true
}

// 聚焦景点 (Leaflet版本)
const focusSpot = (spot) => {
  const map = mapInstance || mapRef.value?.getMap()
  if (map && spot.coords) {
    // hot spots的coords格式是 [lat, lng]
    map.flyTo(spot.coords, 15, { duration: 1.5 })
  }
}

// 在地图上查看并关闭弹窗
const focusAndClose = (spot) => {
  spotDialogVisible.value = false
  focusSpot(spot)
}

// 切换景区范围显示
const toggleScenicAreas = async (show) => {
  const map = mapRef.value?.getMap()
  if (!map) return
  
  if (show) {
    try {
      const areas = await api.getScenicAreas()
      if (areas?.features?.length) {
        scenicAreasLayer = L.geoJSON(areas, {
          style: (feature) => ({
            color: feature.properties.color || '#C41E3A',
            weight: 2,
            fillColor: feature.properties.color || '#C41E3A',
            fillOpacity: 0.2
          }),
          onEachFeature: (feature, layer) => {
            layer.bindPopup(`
              <div>
                <h4>${feature.properties.name}</h4>
                <p><strong>${feature.properties.level}</strong></p>
                <p>${feature.properties.description || ''}</p>
              </div>
            `)
          }
        }).addTo(map)
      }
    } catch (e) {
      console.error('加载景区范围失败:', e)
    }
  } else {
    if (scenicAreasLayer) {
      map.removeLayer(scenicAreasLayer)
      scenicAreasLayer = null
    }
  }
}

// 在地图上显示路线
const showRouteOnMap = () => {
  const map = mapRef.value?.getMap()
  if (!map || !routeData.value) {
    console.warn('地图未初始化或路线数据不存在')
    return
  }
  
  // 移除旧路线
  if (routeLineLayer) {
    map.removeLayer(routeLineLayer)
  }
  
  // 获取路线坐标
  let latLngs = []
  
  // 优先使用后端返回的真实路径 (route_line)
  if (routeData.value.route_line && routeData.value.route_line.length > 0) {
    // 后端返回的是 [lng, lat] (GeoJSON标准), Leaflet 需要 [lat, lng]
    latLngs = routeData.value.route_line.map(coord => {
      // 确保坐标是数组且有两个元素
      if (Array.isArray(coord) && coord.length >= 2) {
        return [coord[1], coord[0]]  // 转换为 [lat, lng]
      }
      console.warn('无效的坐标:', coord)
      return null
    }).filter(c => c !== null)
    
    console.log('使用真实导航路径，共', latLngs.length, '个坐标点')
  } else if (routeData.value.spots && routeData.value.spots.length > 0) {
    // 降级：使用景点坐标直线连接
    console.log('使用景点直线连接，共', routeData.value.spots.length, '个景点')
    latLngs = routeData.value.spots.map(spot => {
      if (spot.coords && Array.isArray(spot.coords) && spot.coords.length >= 2) {
        // spots中的坐标应该是 [lng, lat] (GeoJSON标准)
        return [spot.coords[1], spot.coords[0]]  // 转换为 [lat, lng]
      }
      console.warn('景点坐标无效:', spot)
      return null
    }).filter(c => c !== null)
  }
  
  if (latLngs.length < 2) {
    console.error('坐标点不足，无法绘制路线')
    return
  }
  
  // 绘制路线
  routeLineLayer = L.polyline(latLngs, {
    color: '#C41E3A',
    weight: 5,
    opacity: 0.9,
    lineJoin: 'round'
  }).addTo(map)
  
  // 添加景点标记
  if (routeData.value.spots && routeData.value.spots.length > 0) {
    routeData.value.spots.forEach((spot, idx) => {
      if (!spot.coords || !Array.isArray(spot.coords) || spot.coords.length < 2) {
        console.warn('跳过无效景点:', spot)
        return
      }
      
      const latLng = [spot.coords[1], spot.coords[0]]  // 转换为 [lat, lng]
      
      // 起点绿色，终点红色，中间点金色
      const color = idx === 0 ? '#4CAF50' : 
                    idx === routeData.value.spots.length - 1 ? '#F44336' : 
                    '#FFD700'
      
      L.circleMarker(latLng, {
        radius: 8,
        fillColor: color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 1
      }).bindPopup(`<b>${idx + 1}. ${spot.name}</b><br>${spot.description || ''}`).addTo(map)
    })
  }
  
  // 缩放到路线范围
  try {
    map.fitBounds(L.latLngBounds(latLngs), { padding: [50, 50] })
    console.log('路线显示成功')
  } catch (error) {
    console.error('缩放到路线范围失败:', error)
  }
}

// 导出旅游计划
const exportTravelPlan = () => {
  if (!routeData.value) return
  
  const route = routeData.value
  let content = `# ${route.route_name}\n\n`
  content += `**行程概述**: ${route.description}\n\n`
  content += `**总里程**: ${route.total_distance} 公里 | **总时长**: ${Math.floor(route.total_duration / 60)} 小时\n\n`
  content += `---\n\n## 行程安排\n\n`
  
  route.spots?.forEach((spot, idx) => {
    content += `### ${idx + 1}. ${spot.name}\n`
    content += `- **简介**: ${spot.description}\n`
    content += `- **建议游览时间**: ${spot.duration} 分钟\n\n`
  })
  
  if (aiInterpretation.value) {
    content += `---\n\n## AI旅行建议\n\n${aiInterpretation.value}\n`
  }
  
  content += `\n---\n\n*莆田市市情WebGIS系统 - 旅游计划导出*\n*生成时间: ${new Date().toLocaleString()}*`
  
  // 创建下载
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${route.route_name}_旅游计划.md`
  a.click()
  URL.revokeObjectURL(url)
}

// 加载数据
onMounted(async () => {
  try {
    // 加载行政区划
    const districts = await api.getDistricts()
    districtsData.value = districts

    // 加载旅游POI
    const mazuPOI = await api.getPOI('mazu')
    const scenicPOI = await api.getPOI('scenic')
    const govPOI = await api.getPOI('government')
    
    // 合并POI数据
    tourismPOI.value = {
      type: 'FeatureCollection',
      features: [
        ...(mazuPOI?.features || []),
        ...(scenicPOI?.features || []),
        ...(govPOI?.features || [])
      ]
    }

    // 加载默认路线
    await loadRoute()
  } catch (error) {
    console.error('数据加载失败:', error)
    await loadRoute()
  }
})
</script>

<style scoped>
.tourism-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

.route-display {
  position: absolute;
  bottom: 24px;
  left: 16px;
  z-index: 500;
}

.route-info {
  width: 320px;
}

.route-info h4 {
  margin-bottom: 8px;
  color: var(--golden);
}

.route-info p {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.route-stats {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: var(--text-muted);
}

.route-stats strong {
  color: var(--mazu-red);
  font-size: 16px;
}

.tourism-panel {
  width: 380px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.route-selector h4,
.spots-section h4,
.ai-interpretation h4,
.hot-spots h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.route-selector :deep(.el-radio-button__inner) {
  background: var(--bg-card);
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.route-selector :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: var(--mazu-red);
  border-color: var(--mazu-red);
  color: white;
}

/* 景点时间线 */
.spots-timeline {
  display: flex;
  flex-direction: column;
}

.spot-item {
  display: flex;
  gap: 12px;
}

.spot-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.marker-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--mazu-red), var(--golden));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.marker-line {
  width: 2px;
  flex: 1;
  min-height: 40px;
  background: var(--border-color);
}

.spot-content {
  flex: 1;
  padding-bottom: 16px;
}

.spot-content h5 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.spot-content p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.spot-duration {
  font-size: 11px;
  color: var(--golden);
}

/* AI解读 */
.ai-interpretation {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
}

.interpretation-content {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.interpretation-content :deep(strong) {
  color: var(--golden);
}

.ai-btn {
  background: linear-gradient(135deg, var(--mazu-red) 0%, var(--mazu-red-dark) 100%);
  border: none;
  width: 100%;
}

/* 热门景点 */
.spot-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
}

.spot-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.spot-card:hover {
  border-color: var(--mazu-red);
  transform: translateY(-2px);
}

.spot-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.spot-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.spot-name {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}

.spot-type {
  font-size: 10px;
  color: var(--text-muted);
}

/* 景点详情按钮 */
.detail-btn {
  margin-left: auto;
  padding: 4px 12px !important;
  height: 24px !important;
  font-size: 11px !important;
}

/* 景点详情弹窗 */
.spot-detail {
  padding: var(--spacing-md) 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.detail-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.detail-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-type {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.detail-district {
  font-size: 13px;
  color: var(--text-secondary);
}

.detail-body {
  margin-bottom: var(--spacing-lg);
}

.detail-desc {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);
  text-align: justify;
}

.detail-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--spacing-sm);
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.info-label {
  font-size: 12px;
  color: var(--text-muted);
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.detail-footer {
  text-align: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.detail-footer .el-button {
  width: 100%;
}

/* AI智能推荐样式 */
.ai-recommend-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 1px solid rgba(118, 75, 162, 0.3);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.ai-recommend-section h4 {
  margin-bottom: var(--spacing-sm);
  color: #764ba2;
}

.ai-recommend-options {
  margin-bottom: var(--spacing-sm);
}

.ai-recommend-options .el-select {
  width: 100%;
}

.ai-recommend-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.ai-recommend-buttons .el-button {
  flex: 1;
}

/* AI推荐景点列表 */
.ai-spots-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.ai-spots-section h4 {
  margin-bottom: var(--spacing-sm);
  color: var(--golden);
}

.ai-spots-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
}

.ai-spot-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--bg-card-hover);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.ai-spot-item:hover {
  background: rgba(118, 75, 162, 0.15);
  transform: translateX(4px);
}

.ai-spot-index {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
}

.ai-spot-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.ai-spot-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.ai-spot-desc {
  font-size: 11px;
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.show-all-btn {
  width: 100%;
}

/* 地图上AI标记的样式 */
.ai-spot-marker {
  background: transparent !important;
  border: none !important;
}

/* DIY路线规划样式 */
.diy-route-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.diy-route-section h4 {
  margin: 0 0 var(--spacing-md);
  color: var(--primary);
  font-size: 15px;
}

.travel-mode-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  flex-wrap: wrap;
}

.mode-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.route-spots-list {
  min-height: 60px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.route-spot-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 8px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  border: 1px solid var(--border-color);
}

.route-spot-item:last-child {
  margin-bottom: 0;
}

.route-spot-index {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.route-spot-info {
  flex: 1;
  min-width: 0;
  cursor: pointer;
}

.route-spot-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.route-spot-duration {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
}

.empty-route-hint {
  text-align: center;
  padding: 20px;
  color: var(--text-muted);
  font-size: 12px;
}

.route-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.route-result-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--radius-sm);
  padding: var(--spacing-md);
  color: white;
}

.route-result-info .info-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 4px;
}

.route-result-info .info-row:last-child {
  margin-bottom: 0;
}

.meizhou-entry {
  background: linear-gradient(135deg, #00b8a9 0%, #008378 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 184, 169, 0.2);
  margin-bottom: var(--spacing-lg);
}

.meizhou-entry:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 184, 169, 0.3);
}

.meizhou-entry .entry-content h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  color: white;
}

.meizhou-entry .entry-content p {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
  color: white;
}

.entry-icon {
  font-size: 24px;
  font-weight: bold;
}
</style>
