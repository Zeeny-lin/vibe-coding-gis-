<template>
  <div class="transport-view">
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="null"
        :showLayerControl="false"
        @mapReady="onMapReady"
      />
      
      <!-- 交通图层控制面板 -->
      <div class="transport-layer-control">
        <div class="control-header">🗺️ 图层控制</div>
        <div class="layer-toggles">
          <label class="layer-toggle">
            <input type="checkbox" v-model="layerVisibility.railway" @change="toggleLayer('railway')">
            <span class="toggle-icon railway">🚄</span>
            <span>铁路线路</span>
          </label>
          <label class="layer-toggle">
            <input type="checkbox" v-model="layerVisibility.stations" @change="toggleLayer('stations')">
            <span class="toggle-icon station">🚉</span>
            <span>火车站</span>
          </label>
          <label class="layer-toggle">
            <input type="checkbox" v-model="layerVisibility.highway" @change="toggleLayer('highway')">
            <span class="toggle-icon highway">🛣️</span>
            <span>高速公路</span>
          </label>
          <label class="layer-toggle">
            <input type="checkbox" v-model="layerVisibility.ports" @change="toggleLayer('ports')">
            <span class="toggle-icon port">⚓</span>
            <span>港口码头</span>
          </label>
        </div>
      </div>
    </div>

    <!-- 右侧面板 -->
    <div class="transport-panel">
      <div class="panel-header">
        <span class="panel-title">🚛 综合交通概况</span>
      </div>

      <el-tabs v-model="activeTab" class="transport-tabs">
        <!-- 铁路 -->
        <el-tab-pane label="铁路" name="railway">
          <div class="data-section" v-if="railwayData">
            <div class="stat-grid">
              <div class="stat-item">
                <span class="val">{{ railwayData.total_mileage }}</span>
                <span class="lbl">里程(km)</span>
              </div>
              <div class="stat-item">
                <span class="val">{{ railwayData.total_stations }}</span>
                <span class="lbl">站点(个)</span>
              </div>
            </div>
            
            <div class="list-section">
              <h5>主要线路</h5>
              <div class="tag-cloud">
                <el-tag v-for="line in railwayData.lines" :key="line" effect="dark">{{ line }}</el-tag>
              </div>
              
              <h5 class="mt-4">站点列表</h5>
              <div class="station-list">
                <div class="station-card" v-for="st in railwayData.stations" :key="st.name" @click="focusLocation(st.coordinates)">
                  <div class="st-header">
                    <span class="st-name">{{ st.name }}</span>
                    <el-tag size="small" type="success">{{ st.level }}</el-tag>
                  </div>
                  <div class="st-desc">{{ st.description }}</div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 公路 -->
        <el-tab-pane label="公路" name="highway">
           <div class="data-section" v-if="highwayData">
            <div class="stat-grid three-col">
              <div class="stat-item">
                <span class="val">{{ highwayData.expressway_mileage }}</span>
                <span class="lbl">高速(km)</span>
              </div>
              <div class="stat-item">
                <span class="val">{{ highwayData.national_road_mileage }}</span>
                <span class="lbl">国道(km)</span>
              </div>
              <div class="stat-item">
                <span class="val">{{ highwayData.provincial_road_mileage }}</span>
                <span class="lbl">省道(km)</span>
              </div>
            </div>

             <div class="list-section">
              <h5>主要高速</h5>
              <div class="road-list">
                <div class="road-item" v-for="road in highwayData.roads" :key="road.code">
                  <div class="road-code">{{ road.code }}</div>
                  <div class="road-info">
                    <div class="road-name">{{ road.name }}</div>
                    <div class="road-desc">{{ road.description }}</div>
                  </div>
                </div>
              </div>
            </div>
           </div>
        </el-tab-pane>

        <!-- 港口 -->
        <el-tab-pane label="港口" name="port">
           <div class="data-section" v-if="portData">
             <div class="stat-grid">
              <div class="stat-item">
                <span class="val">{{ portData.annual_cargo }}</span>
                <span class="lbl">年吞吐(万吨)</span>
              </div>
              <div class="stat-item">
                <span class="val">{{ portData.total_berths }}</span>
                <span class="lbl">泊位数</span>
              </div>
            </div>

            <div class="list-section">
              <h5>主要港区</h5>
               <div class="port-list">
                <div class="port-card" v-for="p in portData.ports" :key="p.name" @click="focusLocation(p.coordinates)">
                  <div class="port-icon">⚓</div>
                  <div class="port-info">
                    <div class="port-name">{{ p.name }}</div>
                    <div class="port-type">{{ p.type }}</div>
                  </div>
                </div>
              </div>
            </div>
           </div>
        </el-tab-pane>

        <!-- 时刻表 -->
        <el-tab-pane label="📅 时刻表" name="schedules">
          <div class="schedule-section">
            <el-radio-group v-model="scheduleType" class="schedule-type-select">
              <el-radio-button value="train">🚄 火车</el-radio-button>
              <el-radio-button value="ferry">⛴️ 轮渡</el-radio-button>
              <el-radio-button value="bus">🚌 汽车</el-radio-button>
            </el-radio-group>

            <!-- 火车时刻表 -->
            <div v-if="scheduleType === 'train'" class="schedule-list">
              <div class="schedule-header">
                <span>车次</span><span>始发</span><span>终到</span><span>发车</span><span>到达</span><span>用时</span>
              </div>
              <div class="schedule-row" v-for="s in trainSchedules" :key="s.train_no">
                <span class="train-no">{{ s.train_no }}</span>
                <span>{{ s.from }}</span>
                <span>{{ s.to }}</span>
                <span class="time">{{ s.depart }}</span>
                <span class="time">{{ s.arrive }}</span>
                <span class="duration">{{ s.duration }}</span>
              </div>
            </div>

            <!-- 轮渡时刻表 -->
            <div v-if="scheduleType === 'ferry'" class="schedule-list">
              <div class="schedule-header ferry">
                <span>航线</span><span>发船</span><span>到达</span><span>类型</span><span>票价</span>
              </div>
              <div class="schedule-row" v-for="(s, i) in ferrySchedules" :key="i">
                <span class="route">{{ s.route }}</span>
                <span class="time">{{ s.depart }}</span>
                <span class="time">{{ s.arrive }}</span>
                <span>{{ s.type }}</span>
                <span class="price">{{ s.price }}</span>
              </div>
            </div>

            <!-- 汽车时刻表 -->
            <div v-if="scheduleType === 'bus'" class="schedule-list">
              <div class="schedule-header bus">
                <span>线路</span><span>发车</span><span>到达</span><span>类型</span><span>票价</span>
              </div>
              <div class="schedule-row" v-for="(s, i) in busSchedules" :key="i">
                <span class="route">{{ s.route }}</span>
                <span class="time">{{ s.depart }}</span>
                <span class="time">{{ s.arrive }}</span>
                <span>{{ s.type }}</span>
                <span class="price">{{ s.price }}</span>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 交通分析 -->
        <el-tab-pane label="📊 分析" name="analysis">
          <div class="analysis-section">
            <h5>日均班次统计</h5>
            <div ref="analysisChartRef" class="analysis-chart"></div>
            <div class="analysis-summary">
              <div class="summary-item">
                <span class="label">火车日均班次</span>
                <span class="value">{{ statistics?.daily_train_services || 156 }}</span>
              </div>
              <div class="summary-item">
                <span class="label">轮渡日均班次</span>
                <span class="value">{{ statistics?.daily_ferry_services || 30 }}</span>
              </div>
              <div class="summary-item">
                <span class="label">汽车日均班次</span>
                <span class="value">{{ statistics?.daily_bus_services || 280 }}</span>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 统计指标 -->
      <div class="stats-footer" v-if="statistics">
        <h4>关键指标</h4>
        <div class="kpi-item">
          <span>路网密度:</span>
          <strong>{{ statistics.highway_density }} km/km²</strong>
        </div>
        <div class="kpi-item">
          <span>交通便利指数:</span>
          <strong>{{ statistics.transport_convenience_index }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import L from 'leaflet'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

const mapRef = ref(null)
const analysisChartRef = ref(null)
const districtsData = ref(null)
const transportPOI = ref(null)
const railwayData = ref(null)
const highwayData = ref(null)
const portData = ref(null)
const statistics = ref(null)
const activeTab = ref('railway')
const scheduleType = ref('train')
const trainSchedules = ref([])
const ferrySchedules = ref([])
const busSchedules = ref([])
let chart = null
let mapInstance = null

// 图层可见性控制
const layerVisibility = ref({
  railway: true,
  stations: true,
  highway: true,
  ports: true
})

// 存储各图层引用
const transportLayers = {
  railway: null,
  stations: null,
  highway: null,
  ports: null
}

// 创建火车站图标
const createStationIcon = (name, level) => {
  const isMainStation = level === '一等站' || name.includes('莆田')
  const size = isMainStation ? 36 : 28
  const bgColor = isMainStation ? '#E91E63' : '#2196F3'
  
  return L.divIcon({
    className: 'custom-station-icon',
    html: `<div style="
      background: ${bgColor};
      width: ${size}px;
      height: ${size}px;
      border-radius: 6px;
      border: 3px solid white;
      box-shadow: 0 3px 10px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: ${isMainStation ? 18 : 14}px;
      font-weight: bold;
    ">🚉</div>`,
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
    popupAnchor: [0, -size/2]
  })
}

// 创建港口图标
const createPortIcon = (portType) => {
  const isPassenger = portType.includes('客运')
  const size = isPassenger ? 32 : 26
  const bgColor = isPassenger ? '#00BCD4' : '#607D8B'
  
  return L.divIcon({
    className: 'custom-port-icon',
    html: `<div style="
      background: ${bgColor};
      width: ${size}px;
      height: ${size}px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 3px 10px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: ${size > 28 ? 16 : 12}px;
    ">⚓</div>`,
    iconSize: [size, size],
    iconAnchor: [size/2, size/2],
    popupAnchor: [0, -size/2]
  })
}

// 地图就绪回调
const onMapReady = (map) => {
  mapInstance = map
}

// 初始化交通图层
const initTransportLayers = () => {
  if (!mapInstance) return
  
  // 移除已有图层
  Object.values(transportLayers).forEach(layer => {
    if (layer && mapInstance.hasLayer(layer)) {
      mapInstance.removeLayer(layer)
    }
  })
  
  // 1. 铁路线路图层
  if (transportPOI.value?.features) {
    const railwayFeatures = transportPOI.value.features.filter(
      f => f.properties?.subtype === 'railway' && f.geometry?.type === 'LineString'
    )
    if (railwayFeatures.length > 0) {
      transportLayers.railway = L.geoJSON({
        type: 'FeatureCollection',
        features: railwayFeatures
      }, {
        style: { color: '#000000', weight: 5, dashArray: '10, 8', opacity: 0.8 }
      })
      if (layerVisibility.value.railway) transportLayers.railway.addTo(mapInstance)
    }
  }
  
  // 2. 高速公路图层
  if (transportPOI.value?.features) {
    const highwayFeatures = transportPOI.value.features.filter(
      f => f.properties?.subtype === 'highway' && f.geometry?.type === 'LineString'
    )
    if (highwayFeatures.length > 0) {
      transportLayers.highway = L.geoJSON({
        type: 'FeatureCollection',
        features: highwayFeatures
      }, {
        style: { color: '#FF9800', weight: 5, opacity: 0.85 }
      })
      if (layerVisibility.value.highway) transportLayers.highway.addTo(mapInstance)
    }
  }
  
  // 3. 火车站图层
  if (railwayData.value?.stations) {
    const stationMarkers = railwayData.value.stations.map(station => {
      const coords = station.coordinates
      // coordinates 格式可能是 [lng, lat] 或 [lat, lng]，需要判断
      const lat = coords[1] > 90 ? coords[0] : coords[1]
      const lng = coords[1] > 90 ? coords[1] : coords[0]
      
      return L.marker([lat, lng], {
        icon: createStationIcon(station.name, station.level)
      }).bindPopup(`
        <div style="min-width: 180px;">
          <h4 style="margin: 0 0 8px; color: #E91E63;">🚉 ${station.name}</h4>
          <p style="margin: 4px 0; font-size: 13px;"><strong>等级:</strong> ${station.level}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>线路:</strong> ${station.lines?.join(', ') || '-'}</p>
          <p style="margin: 4px 0; font-size: 12px; color: #666;">${station.description || ''}</p>
        </div>
      `)
    })
    transportLayers.stations = L.layerGroup(stationMarkers)
    if (layerVisibility.value.stations) transportLayers.stations.addTo(mapInstance)
  }
  
  // 4. 港口图层
  if (portData.value?.ports) {
    const portMarkers = portData.value.ports.map(port => {
      const coords = port.coordinates
      const lat = coords[1] > 90 ? coords[0] : coords[1]
      const lng = coords[1] > 90 ? coords[1] : coords[0]
      
      return L.marker([lat, lng], {
        icon: createPortIcon(port.type)
      }).bindPopup(`
        <div style="min-width: 160px;">
          <h4 style="margin: 0 0 8px; color: #00BCD4;">⚓ ${port.name}</h4>
          <p style="margin: 4px 0; font-size: 13px;"><strong>类型:</strong> ${port.type}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>区域:</strong> ${port.district || '-'}</p>
          ${port.annual_cargo ? `<p style="margin: 4px 0; font-size: 12px;">年吞吐量: ${port.annual_cargo}万吨</p>` : ''}
        </div>
      `)
    })
    transportLayers.ports = L.layerGroup(portMarkers)
    if (layerVisibility.value.ports) transportLayers.ports.addTo(mapInstance)
  }
}

// 切换图层显示
const toggleLayer = (layerType) => {
  if (!mapInstance || !transportLayers[layerType]) return
  
  if (layerVisibility.value[layerType]) {
    transportLayers[layerType].addTo(mapInstance)
  } else {
    mapInstance.removeLayer(transportLayers[layerType])
  }
}

const focusLocation = (coords) => {
  if (mapRef.value && coords) {
    const map = mapRef.value.getMap()
    map.setView([coords[1], coords[0]], 13)
  }
}

// 初始化分析图表
const initAnalysisChart = () => {
  if (!analysisChartRef.value) return
  
  chart = echarts.init(analysisChartRef.value)
  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: { data: ['火车', '轮渡', '汽车'], textStyle: { color: '#a0a0b0' }, top: 0 },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      name: '班次',
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0' },
      splitLine: { lineStyle: { color: '#2a2a4a' } }
    },
    series: [
      { name: '火车', type: 'line', smooth: true, data: [8, 25, 18, 12, 15, 22, 28, 10], itemStyle: { color: '#E91E63' } },
      { name: '轮渡', type: 'line', smooth: true, data: [2, 4, 3, 2, 4, 4, 3, 2], itemStyle: { color: '#2196F3' } },
      { name: '汽车', type: 'line', smooth: true, data: [15, 35, 28, 20, 25, 32, 38, 18], itemStyle: { color: '#FF9800' } }
    ]
  }
  chart.setOption(option)
}

// 监听tab切换
watch(activeTab, async (val) => {
  if (val === 'analysis') {
    await nextTick()
    initAnalysisChart()
  }
})

onMounted(async () => {
  try {
    const [districts, transportGeo, rail, high, port, stats, trainSched, ferrySched, busSched] = await Promise.all([
      api.getDistricts(),
      api.getTransportGeojson().catch(() => null),
      api.getRailway(),
      api.getHighway(),
      api.getPorts(),
      api.getTransport(),
      api.getTrainSchedules().catch(() => ({ schedules: [] })),
      api.getFerrySchedules().catch(() => ({ schedules: [] })),
      api.getBusSchedules().catch(() => ({ schedules: [] }))
    ])

    districtsData.value = districts
    transportPOI.value = transportGeo
    railwayData.value = rail
    highwayData.value = high
    portData.value = port
    trainSchedules.value = trainSched?.schedules || []
    ferrySchedules.value = ferrySched?.schedules || []
    busSchedules.value = busSched?.schedules || []
    
    if (stats && stats.statistics) {
      statistics.value = stats.statistics
    }
    
    // 等待地图就绪后初始化图层
    await nextTick()
    setTimeout(() => {
      if (!mapInstance && mapRef.value) {
        mapInstance = mapRef.value.getMap()
      }
      initTransportLayers()
    }, 500)
  } catch (error) {
    console.error('加载交通数据失败:', error)
    // 模拟数据 fallback
    railwayData.value = {
      total_mileage: 185,
      total_stations: 4,
      lines: ['福厦铁路', '向莆铁路', '福厦高铁'],
      stations: [
        { name: '莆田站', level: '一等站', description: '福厦铁路、向莆铁路主要客运站', coordinates: [25.43, 119.01] },
        { name: '仙游站', level: '三等站', description: '福厦铁路沿线站点', coordinates: [25.35, 118.72] },
        { name: '涵江站', level: '三等站', description: '福厦铁路沿线站点', coordinates: [25.48, 119.10] }
      ]
    }
    
    highwayData.value = {
      expressway_mileage: 268,
      national_road_mileage: 350,
      provincial_road_mileage: 480,
      roads: [
        { code: 'G15', name: '沈海高速', description: '贯穿南北主要通道' },
        { code: 'G1517', name: '莆炎高速', description: '连接内陆重要通道' },
        { code: 'G324', name: '福昆线', description: '主要干线公路' }
      ]
    }
    
    portData.value = {
      annual_cargo: 5800,
      total_berths: 45,
      ports: [
        { name: '秀屿港区', type: '综合性港区', coordinates: [25.26, 119.12] },
        { name: '东吴港区', type: '大宗散货港区', coordinates: [25.20, 119.15] },
        { name: '兴化港区', type: '临港工业港区', coordinates: [25.32, 119.20] }
      ]
    }
    
    statistics.value = {
      daily_train_services: 156,
      daily_ferry_services: 32,
      daily_bus_services: 280,
      highway_density: 1.52,
      transport_convenience_index: 8.5
    }

    // 默认时刻表
    trainSchedules.value = [
      { train_no: 'D6201', from: '福州', to: '厦门', depart: '08:00', arrive: '08:45', duration: '45分' },
      { train_no: 'G1602', from: '深圳北', to: '福州南', depart: '09:20', arrive: '09:55', duration: '35分' },
      { train_no: 'D3103', from: '杭州东', to: '厦门北', depart: '10:15', arrive: '10:58', duration: '43分' }
    ]
    ferrySchedules.value = [
      { route: '文甲-湄洲', depart: '07:30', arrive: '07:45', type: '快艇', price: '￥60' },
      { route: '文甲-湄洲', depart: '08:00', arrive: '08:15', type: '客船', price: '￥45' }
    ]
    busSchedules.value = [
      { route: 'K01路', depart: '06:00', arrive: '22:00', type: '公交', price: '￥2' },
      { route: '36路', depart: '06:30', arrive: '21:30', type: '公交', price: '￥1' }
    ]
  }
})
</script>

<style scoped>
.transport-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

/* 交通图层控制面板 */
.transport-layer-control {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  min-width: 150px;
}

.control-header {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.layer-toggles {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.2s;
}

.layer-toggle:hover {
  color: var(--text-primary);
}

.layer-toggle input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #2196F3;
}

.toggle-icon {
  font-size: 16px;
}

.legend-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: var(--bg-card);
  padding: 10px;
  border-radius: 4px;
  z-index: 500;
  border: 1px solid var(--border-color);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.dot.rail { background: #E91E63; }
.dot.port { background: #2196F3; }
.dot.road { background: #FF9800; }

.transport-panel {
  width: 380px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
}

.panel-title {
  color: #2196F3; /* 蓝色主题 */
  font-size: 18px;
  font-weight: 600;
}

.transport-tabs :deep(.el-tabs__item) {
  color: var(--text-secondary);
}

.transport-tabs :deep(.el-tabs__item.is-active) {
  color: #2196F3;
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.stat-grid.three-col {
  grid-template-columns: 1fr 1fr 1fr;
}

.stat-item {
  background: var(--bg-card);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid var(--border-color);
}

.stat-item .val {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #2196F3;
}

.stat-item .lbl {
  font-size: 12px;
  color: var(--text-muted);
}

.tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }

.mt-4 { margin-top: 16px; }

.station-list, .port-list, .road-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

/* 列表卡片样式 */
.station-card, .port-card, .road-item {
  background: var(--bg-card);
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.station-card:hover, .port-card:hover, .road-item:hover {
  border-color: #2196F3;
  transform: translateX(4px);
}

.st-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.st-name { font-weight: 500; color: var(--text-primary); }
.st-desc { font-size: 12px; color: var(--text-secondary); }

/* 公路样式 */
.road-item { display: flex; gap: 10px; align-items: flex-start; }
.road-code {
  background: #FF9800;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}
.road-info { flex: 1; }
.road-name { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.road-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* 港口样式 */
.port-card { display: flex; align-items: center; gap: 12px; }
.port-icon { font-size: 24px; }
.port-name { font-size: 14px; font-weight: 500; }
.port-type { font-size: 12px; color: var(--text-muted); }

/* 底部统计 */
.stats-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.stats-footer h4 { margin-bottom: 12px; font-size: 14px; color: var(--text-primary); }

.kpi-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.kpi-item strong { color: #2196F3; }

/* 时刻表样式 */
.schedule-section { padding: 10px 0; }
.schedule-type-select { margin-bottom: 16px; }
.schedule-type-select :deep(.el-radio-button__inner) {
  background: var(--bg-card);
  border-color: var(--border-color);
  color: var(--text-secondary);
  font-size: 12px;
  padding: 8px 12px;
}
.schedule-type-select :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: #2196F3;
  border-color: #2196F3;
  color: white;
}

.schedule-list {
  max-height: 400px;
  overflow-y: auto;
}

.schedule-header {
  display: grid;
  grid-template-columns: 1fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr;
  gap: 4px;
  padding: 8px;
  background: var(--bg-card);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.schedule-header.ferry, .schedule-header.bus {
  grid-template-columns: 1.5fr 0.8fr 0.8fr 0.8fr 0.8fr;
}

.schedule-row {
  display: grid;
  grid-template-columns: 1fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr;
  gap: 4px;
  padding: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
  transition: background 0.2s;
}

.schedule-row:hover { background: var(--bg-card); }

.schedule-list .schedule-row:has(.route) {
  grid-template-columns: 1.5fr 0.8fr 0.8fr 0.8fr 0.8fr;
}

.train-no { color: #E91E63; font-weight: 600; }
.time { color: #2196F3; font-weight: 500; }
.duration { color: var(--golden); font-size: 11px; }
.route { font-weight: 500; }
.price { color: #4CAF50; font-weight: 500; }

/* 分析图表 */
.analysis-section h5 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.analysis-chart {
  height: 200px;
  margin-bottom: 16px;
}

.analysis-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.summary-item {
  background: var(--bg-card);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid var(--border-color);
}

.summary-item .label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.summary-item .value {
  font-size: 20px;
  font-weight: 700;
  color: #2196F3;
}
</style>
