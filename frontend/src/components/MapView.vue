<template>
  <div class="map-wrapper">
    <div ref="mapContainer" class="map-view"></div>
    
    <!-- 地图控制按钮 -->
    <div class="map-controls">
      <el-button-group>
        <el-button size="small" @click="zoomIn">
          <el-icon><Plus /></el-icon>
        </el-button>
        <el-button size="small" @click="zoomOut">
          <el-icon><Minus /></el-icon>
        </el-button>
        <el-button size="small" @click="resetView">
          <el-icon><Aim /></el-icon>
        </el-button>
      </el-button-group>
    </div>

    <!-- 图层控制 -->
    <div class="layer-control" v-if="showLayerControl">
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">图层控制</span>
        </div>
        
        <!-- 底图选择 -->
        <div class="control-section">
          <div class="section-title">底图选择</div>
          <el-radio-group v-model="currentBaseLayer" @change="changeBaseLayer" class="base-layer-select">
            <el-radio label="amap_normal">高德标准</el-radio>
            <el-radio label="amap_satellite">高德卫星</el-radio>
          </el-radio-group>
        </div>

        <div class="divider"></div>

        <!-- 覆盖图层 -->
        <div class="control-section">
          <div class="section-title">覆盖图层</div>
          <div class="layer-list">
            <el-checkbox 
              v-for="layer in layers" 
              :key="layer.id"
              v-model="layer.visible"
              @change="toggleLayer(layer)"
            >
              {{ layer.name }}
            </el-checkbox>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import { Plus, Minus, Aim } from '@element-plus/icons-vue'

const props = defineProps({
  center: {
    type: Array,
    default: () => [25.4, 119.0]  // 莆田市中心
  },
  zoom: {
    type: Number,
    default: 10
  },
  geojsonData: {
    type: Object,
    default: null
  },
  poiData: {
    type: Object,
    default: null
  },
  showLayerControl: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['mapReady', 'featureClick'])

const mapContainer = ref(null)
let map = null

// 底图管理
const currentBaseLayer = ref('amap_normal')
const baseLayers = {}

// 切换底图
const changeBaseLayer = (type) => {
  if (!map) return
  
  // 移除所有底图
  Object.values(baseLayers).forEach(layer => {
    if (map.hasLayer(layer)) {
      map.removeLayer(layer)
    }
  })
  
  // 添加选中底图
  if (baseLayers[type]) {
    baseLayers[type].addTo(map)
  }
}

// 图层管理
const layers = ref([
  { id: 'districts', name: '行政区划', visible: true, layer: null },
  { id: 'mazu', name: '妈祖文化', visible: true, layer: null },
  { id: 'school', name: '教育机构', visible: true, layer: null },
  { id: 'hospital', name: '医疗机构', visible: true, layer: null },
  { id: 'scenic', name: '风景名胜', visible: true, layer: null },
  { id: 'transport', name: '交通路网', visible: true, layer: null },
  { id: 'other', name: '其他地点', visible: false, layer: null }
])

// 妈祖文化主题样式
const districtStyle = {
  color: '#C41E3A',
  weight: 2,
  fillColor: '#C41E3A',
  fillOpacity: 0.1
}

const districtHoverStyle = {
  color: '#FFD700',
  weight: 3,
  fillOpacity: 0.3
}

// 初始化地图
onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
  }
})

const initMap = () => {
  // 创建地图实例
  map = L.map(mapContainer.value, {
    center: props.center,
    zoom: props.zoom,
    zoomControl: false,
    attributionControl: false
  })

  // 初始化底图
  // 1. 高德标准图
  baseLayers.amap_normal = L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    maxZoom: 18,
    subdomains: ['1', '2', '3', '4']
  })
  
  // 2. 高德卫星影像
  baseLayers.amap_satellite = L.tileLayer('https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', {
    maxZoom: 18,
    subdomains: ['1', '2', '3', '4']
  })

  // 默认添加高德标准底图
  baseLayers.amap_normal.addTo(map)

  // 发送地图就绪事件
  emit('mapReady', map)

  // 如果有初始数据，加载它
  if (props.geojsonData) {
    loadGeoJSON(props.geojsonData)
  }

  if (props.poiData) {
    loadPOI(props.poiData)
  }
}

// 加载GeoJSON数据
const loadGeoJSON = (data) => {
  if (!map || !data) return

  const geojsonLayer = L.geoJSON(data, {
    style: districtStyle,
    onEachFeature: (feature, layer) => {
      // 添加弹出信息
      // 这里的popup是基于点击位置的，不会与右上角固定面板冲突
      // 但为了避免视觉干扰，我们在HomeView中主要依靠左侧面板展示信息
      // 点击事件已经通过featureClick发出
      
      // 鼠标悬停效果
      layer.on({
        mouseover: (e) => {
          e.target.setStyle(districtHoverStyle)
        },
        mouseout: (e) => {
          geojsonLayer.resetStyle(e.target)
        },
        click: (e) => {
          // 这里我们阻止默认的popup，改用HomeView的侧边面板
          // 这样可以彻底避免重叠问题
          L.DomEvent.stopPropagation(e)
          emit('featureClick', feature.properties)
        }
      })
    }
  }).addTo(map)

  // 存储图层引用
  const districtLayerConfig = layers.value.find(l => l.id === 'districts')
  if (districtLayerConfig) {
    districtLayerConfig.layer = geojsonLayer
  }

  // 缩放到数据范围
  map.fitBounds(geojsonLayer.getBounds(), { padding: [20, 20] })
}

// 加载POI数据
const loadPOI = (data) => {
  if (!map || !data) return

  // 1. 清理现有POI图层
  layers.value.forEach(layerConfig => {
    if (layerConfig.id !== 'districts' && layerConfig.layer) {
      map.removeLayer(layerConfig.layer)
      layerConfig.layer = null
    }
  })

  // 2. 对Feature分类
  const featuresByType = {
    mazu: [],
    school: [],
    hospital: [],
    scenic: [],
    transport: [],
    other: []
  }

  const features = data.features || []
  features.forEach(feature => {
    const type = feature.properties.type
    const subtype = feature.properties.subtype

    if (subtype === 'railway' || subtype === 'highway') {
      featuresByType.transport.push(feature)
    } else if (featuresByType[type]) {
      featuresByType[type].push(feature)
    } else {
      featuresByType.other.push(feature)
    }
  })

  // 3. 创建各分类图层
  const createIcon = (type, level) => {
    // 基础颜色配置
    const baseColors = {
      mazu: '#C41E3A',
      hospital: '#00A8E8',
      school: '#00C853',
      scenic: '#FFD700',
      other: '#9E9E9E'
    }
    
    // 医院等级颜色
    const hospitalLevelColors = {
      '三甲医院': '#E91E63',
      '二甲医院': '#2196F3',
      '一级医院': '#4CAF50',
      '专科医院': '#9C27B0',
      '综合医院': '#607D8B'
    }
    
    // 学校等级颜色
    const schoolLevelColors = {
      '高等院校': '#E91E63',
      '高中': '#FF5722',
      '中学': '#2196F3',
      '初中': '#03A9F4',
      '小学': '#4CAF50',
      '职业学校': '#9C27B0',
      '幼儿园': '#FFEB3B',
      '其他学校': '#607D8B'
    }
    
    // 根据类型和等级选择颜色
    let color = baseColors[type] || '#9E9E9E'
    if (type === 'hospital' && level && hospitalLevelColors[level]) {
      color = hospitalLevelColors[level]
    } else if (type === 'school' && level && schoolLevelColors[level]) {
      color = schoolLevelColors[level]
    }
    
    // 根据等级调整图标大小 - 使用偶数确保锚点居中
    let size = 12
    if (level === '三甲医院' || level === '高等院校') size = 16
    else if (level === '二甲医院' || level === '高中' || level === '中学') size = 14
    
    // 使用圆形标记图标 - 改用circleMarker风格的简单圆点
    const anchor = Math.floor(size / 2)
    
    return L.divIcon({
      className: 'leaflet-poi-marker',
      html: `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <circle cx="${anchor}" cy="${anchor}" r="${anchor - 1}" fill="${color}" stroke="white" stroke-width="1.5"/>
      </svg>`,
      iconSize: [size, size],
      iconAnchor: [anchor, anchor]
    })
  }

  // 为每个分类创建图层
  Object.entries(featuresByType).forEach(([type, subFeatures]) => {
    if (subFeatures.length === 0) return

    const layerConfig = layers.value.find(l => l.id === type)
    if (!layerConfig) return

    const geoJSONData = {
      type: 'FeatureCollection',
      features: subFeatures
    }

    const layer = L.geoJSON(geoJSONData, {
      style: getFeatureStyle,
      pointToLayer: (feature, latlng) => {
        const type = feature.properties.type || 'default'
        
        // 颜色配置 - 与图例完全匹配
        const colorMap = {
          mazu: '#C41E3A',      // 妈祖文化 - 红色
          hospital: '#00A8E8',  // 医疗机构 - 蓝色
          school: '#00C853',    // 教育机构 - 绿色
          scenic: '#FFD700',    // 风景名胜 - 金黄色
          transport: '#FF9800', // 交通路网 - 橙色
          other: '#9E9E9E'      // 其他地点 - 灰色
        }
        const color = colorMap[type] || '#9E9E9E'
        
        // 使用circleMarker - 原生支持缩放定位
        return L.circleMarker(latlng, {
          radius: 7,
          fillColor: color,
          color: '#fff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.85
        })
      },
      onEachFeature: (feature, layer) => {
        const props = feature.properties
        layer.bindPopup(`
          <div class="popup-content">
            <h4>${props.name || '未知地点'}</h4>
            ${props.level ? `<p style="color: #E91E63; font-weight: bold;">🏷️ ${props.level}</p>` : ''}
            ${props.address ? `<p>📍 ${props.address}</p>` : ''}
            ${props.district ? `<p>🏘️ ${props.district}</p>` : ''}
            ${props.tel ? `<p>📞 ${props.tel}</p>` : ''}
          </div>
        `)
      }
    })

    // 保存图层引用
    layerConfig.layer = layer

    // 根据配置决定是否添加到地图
    if (layerConfig.visible) {
      layer.addTo(map)
    }
  })
} 

// 处理LineString样式的函数
const getFeatureStyle = (feature) => {
  const subtype = feature.properties.subtype
  if (subtype === 'railway') {
    return { color: '#000000', weight: 4, dashArray: '10, 10', opacity: 0.7 }
  } else if (subtype === 'highway') {
    return { color: '#FF9800', weight: 4, opacity: 0.8 }
  }
  return { color: '#3388ff', weight: 3 }
}

// 图层切换
const toggleLayer = (layerConfig) => {
  if (!map || !layerConfig.layer) return
  
  if (layerConfig.visible) {
    layerConfig.layer.addTo(map)
  } else {
    map.removeLayer(layerConfig.layer)
  }
}

// 地图控制方法
const zoomIn = () => map?.zoomIn()
const zoomOut = () => map?.zoomOut()
const resetView = () => {
  map?.setView(props.center, props.zoom)
}

// 监听数据变化
watch(() => props.geojsonData, (newData) => {
  if (newData) loadGeoJSON(newData)
}, { deep: true })

watch(() => props.poiData, (newData) => {
  if (newData) loadPOI(newData)
}, { deep: true })

// 修改图层样式
const setDistrictStyle = (style) => {
  const districtLayer = layers.value.find(l => l.id === 'districts')?.layer
  if (districtLayer) {
    districtLayer.setStyle(style)
  }
}

// 暴露方法给父组件
defineExpose({
  getMap: () => map,
  loadGeoJSON,
  loadPOI,
  setDistrictStyle,
  fitBounds: (bounds) => map?.fitBounds(bounds)
})
</script>

<style scoped>
.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-view {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 1000;
}

.map-controls .el-button {
  background: var(--bg-card);
  border-color: var(--border-color);
  color: var(--text-primary);
}

.map-controls .el-button:hover {
  background: var(--bg-card-hover);
  border-color: var(--mazu-red);
  color: var(--mazu-red);
}

/* 图层控制改为右下角，避免与右上角的行政区划详情冲突 */
.layer-control {
  position: absolute;
  bottom: 100px;
  right: 16px;
  z-index: 1000;
  width: 200px;
}

.panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-lg);
}

.control-section {
  margin-bottom: 12px;
}

.section-title {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-weight: 600;
}

.divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 12px 0;
}

.base-layer-select {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.base-layer-select .el-radio {
  margin-right: 0;
  height: auto;
  color: var(--text-primary);
}

.layer-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-list .el-checkbox {
  color: var(--text-primary);
  height: auto;
}
</style>

<style>
/* 全局POI图标样式 - SVG方式修复缩放问题 */
.leaflet-poi-marker {
  background: transparent !important;
  border: none !important;
}

.leaflet-poi-marker svg {
  display: block;
}

/* 兼容旧的className */
.custom-poi-icon {
  background: transparent !important;
  border: none !important;
}
</style>
