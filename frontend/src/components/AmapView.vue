<template>
  <div class="amap-wrapper">
    <div ref="mapContainer" class="amap-container"></div>
    
    <!-- 搜索框 -->
    <div class="amap-search-box" v-if="showSearch">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索景点、地点..."
        prefix-icon="Search"
        size="small"
        @keyup.enter="searchPlace"
        clearable
      >
        <template #append>
          <el-button @click="searchPlace">搜索</el-button>
        </template>
      </el-input>
      
      <!-- 搜索结果 -->
      <div class="search-results" v-if="searchResults.length > 0">
        <div 
          class="search-result-item" 
          v-for="(item, idx) in searchResults" 
          :key="idx"
          @click="selectSearchResult(item)"
        >
          <span class="result-name">{{ item.name }}</span>
          <span class="result-address">{{ item.address }}</span>
        </div>
      </div>
    </div>

    <!-- 地图控制按钮 -->
    <div class="amap-controls">
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

    <!-- 图层切换 -->
    <div class="map-type-switch" v-if="showLayerSwitch">
      <el-radio-group v-model="mapType" @change="switchMapType" size="small">
        <el-radio-button label="normal">标准</el-radio-button>
        <el-radio-button label="satellite">卫星</el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Plus, Minus, Aim, Search } from '@element-plus/icons-vue'

const props = defineProps({
  center: {
    type: Array,
    default: () => [119.0, 25.4]  // 莆田市中心 [lng, lat]
  },
  zoom: {
    type: Number,
    default: 10
  },
  showSearch: {
    type: Boolean,
    default: true
  },
  showLayerSwitch: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['mapReady', 'poiClick', 'mapClick'])

const mapContainer = ref(null)
let map = null
let placeSearch = null
let geocoder = null
let infoWindow = null

const searchKeyword = ref('')
const searchResults = ref([])
const mapType = ref('normal')

// 初始化地图
onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.destroy()
  }
})

const initMap = () => {
  if (!window.AMap) {
    console.error('高德地图API未加载')
    return
  }

  // 创建地图实例
  map = new AMap.Map(mapContainer.value, {
    zoom: props.zoom,
    center: props.center,
    viewMode: '2D',
    lang: 'zh_cn',
    features: ['bg', 'road', 'building', 'point'],  // 启用POI点
  })

  // 添加控件
  map.addControl(new AMap.Scale())

  // 初始化搜索服务
  placeSearch = new AMap.PlaceSearch({
    city: '莆田',
    citylimit: true,
    pageSize: 10
  })

  // 初始化地理编码
  geocoder = new AMap.Geocoder({
    city: '莆田'
  })

  // 初始化信息窗口
  infoWindow = new AMap.InfoWindow({
    offset: new AMap.Pixel(0, -30)
  })

  // 地图点击事件
  map.on('click', (e) => {
    const { lng, lat } = e.lnglat
    emit('mapClick', { lng, lat })
    
    // 逆地理编码获取点击位置信息
    geocoder.getAddress([lng, lat], (status, result) => {
      if (status === 'complete' && result.info === 'OK') {
        const address = result.regeocode.formattedAddress
        const content = `
          <div style="padding: 8px; min-width: 200px;">
            <p style="margin: 0 0 8px; font-size: 14px; font-weight: bold;">📍 点击位置</p>
            <p style="margin: 0 0 4px; font-size: 12px;">${address}</p>
            <p style="margin: 0; font-size: 11px; color: #666;">
              经度: ${lng.toFixed(6)}<br>
              纬度: ${lat.toFixed(6)}
            </p>
          </div>
        `
        infoWindow.setContent(content)
        infoWindow.open(map, e.lnglat)
      }
    })
  })

  // POI点击事件（高德地图原生POI）
  map.on('hotspotclick', (e) => {
    const { name, id, lnglat } = e
    emit('poiClick', { name, id, lnglat })
    
    // 显示POI信息
    const content = `
      <div style="padding: 8px; min-width: 180px;">
        <p style="margin: 0 0 8px; font-size: 14px; font-weight: bold;">🏷️ ${name}</p>
        <p style="margin: 0; font-size: 11px; color: #666;">
          点击获取更多信息
        </p>
      </div>
    `
    infoWindow.setContent(content)
    infoWindow.open(map, lnglat)
  })

  emit('mapReady', map)
}

// 搜索地点
const searchPlace = () => {
  if (!searchKeyword.value.trim()) return
  
  placeSearch.search(searchKeyword.value, (status, result) => {
    if (status === 'complete' && result.info === 'OK') {
      searchResults.value = result.poiList.pois.map(poi => ({
        name: poi.name,
        address: poi.address,
        location: poi.location,
        type: poi.type
      }))
    } else {
      searchResults.value = []
    }
  })
}

// 选择搜索结果
const selectSearchResult = (item) => {
  if (item.location) {
    map.setZoomAndCenter(15, [item.location.lng, item.location.lat])
    
    // 显示信息窗口
    const content = `
      <div style="padding: 8px; min-width: 200px;">
        <p style="margin: 0 0 8px; font-size: 14px; font-weight: bold;">🎯 ${item.name}</p>
        <p style="margin: 0 0 4px; font-size: 12px;">${item.address || ''}</p>
        <p style="margin: 0; font-size: 11px; color: #999;">${item.type || ''}</p>
      </div>
    `
    infoWindow.setContent(content)
    infoWindow.open(map, item.location)
  }
  
  searchResults.value = []
  searchKeyword.value = ''
}

// 切换地图类型
const switchMapType = (type) => {
  if (!map) return
  
  if (type === 'satellite') {
    map.setLayers([new AMap.TileLayer.Satellite()])
  } else {
    map.setLayers([new AMap.TileLayer()])
  }
}

// 地图控制
const zoomIn = () => map?.zoomIn()
const zoomOut = () => map?.zoomOut()
const resetView = () => {
  map?.setZoomAndCenter(props.zoom, props.center)
}

// 添加标记
const addMarker = (position, options = {}) => {
  if (!map) return null
  
  const marker = new AMap.Marker({
    position,
    title: options.title || '',
    ...options
  })
  marker.setMap(map)
  return marker
}

// 添加路线
const addPolyline = (path, options = {}) => {
  if (!map) return null
  
  const polyline = new AMap.Polyline({
    path,
    strokeColor: options.color || '#C41E3A',
    strokeWeight: options.weight || 5,
    strokeOpacity: options.opacity || 0.9,
    ...options
  })
  polyline.setMap(map)
  return polyline
}

// 飞到指定位置
const flyTo = (position, zoom = 15) => {
  map?.setZoomAndCenter(zoom, position, true)
}

// 暴露方法给父组件
defineExpose({
  getMap: () => map,
  addMarker,
  addPolyline,
  flyTo,
  fitBounds: (bounds) => map?.setBounds(bounds)
})
</script>

<style scoped>
.amap-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.amap-container {
  width: 100%;
  height: 100%;
}

.amap-search-box {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 1000;
  width: 300px;
}

.amap-search-box .el-input {
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  border-radius: 8px;
}

.search-results {
  background: white;
  border-radius: 8px;
  margin-top: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  max-height: 300px;
  overflow-y: auto;
}

.search-result-item {
  padding: 10px 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.search-result-item:hover {
  background-color: #f5f5f5;
}

.search-result-item:last-child {
  border-bottom: none;
}

.result-name {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.result-address {
  display: block;
  font-size: 12px;
  color: #999;
}

.amap-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 1000;
}

.amap-controls .el-button {
  background: white;
  border-color: #ddd;
  color: #333;
}

.amap-controls .el-button:hover {
  background: #f5f5f5;
  border-color: #C41E3A;
  color: #C41E3A;
}

.map-type-switch {
  position: absolute;
  bottom: 24px;
  right: 16px;
  z-index: 1000;
}

.map-type-switch .el-radio-button__inner {
  background: white;
  border-color: #ddd;
}
</style>
