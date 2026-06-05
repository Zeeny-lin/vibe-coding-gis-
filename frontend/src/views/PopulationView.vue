<template>
  <div class="population-view">
    <!-- 左侧地图区域 -->
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :showLayerControl="false"
        @featureClick="handleDistrictClick"
      />

      <!-- 图例 -->
      <div class="map-legend panel">
        <div class="panel-header">
          <span class="panel-title">人口密度图例</span>
        </div>
        <div class="legend-gradient">
          <div class="gradient-bar"></div>
          <div class="gradient-labels">
            <span>低密度</span>
            <span>高密度</span>
          </div>
        </div>
        <div class="heatmap-toggle">
          <el-checkbox v-model="showHeatmap" @change="toggleHeatmap">
            显示人口密度热力图
          </el-checkbox>
        </div>
      </div>
    </div>

    <!-- 右侧分析面板 -->
    <div class="analysis-panel">
      <div class="panel-header">
        <span class="panel-title">人口分布分析</span>
      </div>

      <!-- 总体概况 -->
      <div class="overview-section">
        <div class="overview-card">
          <span class="card-value">{{ populationData.total_population || 306.8 }}</span>
          <span class="card-label">常住人口(万人)</span>
        </div>
        <div class="overview-card">
          <span class="card-value">{{ averageDensity }}</span>
          <span class="card-label">平均密度(人/km²)</span>
        </div>
      </div>

      <!-- 人口分布图表 -->
      <div class="chart-section">
        <h4>各区县人口分布</h4>
        <div ref="populationChartRef" class="chart-container"></div>
      </div>

      <!-- 人口密度排名 -->
      <div class="ranking-section">
        <h4>人口密度排名</h4>
        <div class="ranking-list">
          <div 
            class="ranking-item" 
            v-for="(district, index) in sortedByDensity" 
            :key="district.name"
            @click="selectDistrict(district)"
          >
            <span class="rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
            <span class="name">{{ district.name }}</span>
            <span class="value">{{ district.population_density }} 人/km²</span>
          </div>
        </div>
      </div>

      <!-- 选中区县详情 -->
      <div class="selected-detail" v-if="selectedDistrict">
        <h4>{{ selectedDistrict.name }} 详情</h4>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="label">常住人口</span>
            <span class="value">{{ selectedDistrict.population }} 万</span>
          </div>
          <div class="detail-item">
            <span class="label">人口密度</span>
            <span class="value">{{ selectedDistrict.population_density }} 人/km²</span>
          </div>
          <div class="detail-item">
            <span class="label">城镇化率</span>
            <span class="value">{{ selectedDistrict.urban_rate }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import L from 'leaflet'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'
import '@/utils/leaflet-heat.js'

const mapRef = ref(null)
const populationChartRef = ref(null)
const districtsData = ref(null)
const populationData = ref({})
const selectedDistrict = ref(null)
const showHeatmap = ref(false)
let chart = null
let heatmapLayer = null

// 区县中心坐标
const districtCenters = {
  '城厢区': [25.43, 118.99],
  '荔城区': [25.43, 119.02],
  '涵江区': [25.46, 119.12],
  '秀屿区': [25.28, 119.10],
  '仙游县': [25.36, 118.69]
}

// 计算平均密度
const averageDensity = computed(() => {
  const districts = populationData.value.districts || []
  if (districts.length === 0) return 730
  const total = districts.reduce((sum, d) => sum + (d.population_density || 0), 0)
  return Math.round(total / districts.length)
})

// 按人口密度排序
const sortedByDensity = computed(() => {
  const districts = populationData.value.districts || []
  return [...districts].sort((a, b) => (b.population_density || 0) - (a.population_density || 0))
})

// 初始化图表
const initChart = () => {
  if (!populationChartRef.value) return
  
  chart = echarts.init(populationChartRef.value)
  
  const districts = populationData.value.districts || []
  const names = districts.map(d => d.name)
  const populations = districts.map(d => d.population)

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLine: { lineStyle: { color: '#dcdfe6' } },
      axisLabel: { color: '#606266', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      name: '人口(万)',
      nameTextStyle: { color: '#606266' },
      axisLine: { lineStyle: { color: '#dcdfe6' } },
      axisLabel: { color: '#606266' },
      splitLine: { lineStyle: { color: '#ebeef5' } }
    },
    series: [{
      name: '人口',
      type: 'bar',
      data: populations,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#C41E3A' },
          { offset: 1, color: '#9A1830' }
        ]),
        borderRadius: [4, 4, 0, 0]
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#FFD700' },
            { offset: 1, color: '#C5A000' }
          ])
        }
      }
    }]
  }

  chart.setOption(option)
}

// 加载数据
onMounted(async () => {
  try {
    // 加载行政区划
    const districts = await api.getDistricts()
    districtsData.value = districts

    // 加载人口统计
    const population = await api.getPopulationStats()
    populationData.value = population

    await nextTick()
    initChart()
  } catch (error) {
    console.error('数据加载失败:', error)
    // 使用模拟数据
    // 使用其真实数据作为Fallback (以防后端API暂时未重启)
    populationData.value = {
      total_population: 319.2,
      districts: [
        { name: '城厢区', population: 54.42, population_density: 1200, urban_rate: 88.5 },
        { name: '涵江区', population: 47.60, population_density: 780, urban_rate: 74.2 },
        { name: '荔城区', population: 67.01, population_density: 2300, urban_rate: 93.5 },
        { name: '秀屿区', population: 60.07, population_density: 710, urban_rate: 60.2 },
        { name: '仙游县', population: 90.10, population_density: 480, urban_rate: 54.1 }
      ]
    }
    await nextTick()
    initChart()
  }
})

// 处理区县点击
const handleDistrictClick = (properties) => {
  const district = populationData.value.districts?.find(d => d.name === properties.name)
  selectedDistrict.value = district || properties
}

// 选择区县
const selectDistrict = (district) => {
  selectedDistrict.value = district
}

// 切换热力图显示
const toggleHeatmap = (show) => {
  const map = mapRef.value?.getMap()
  if (!map) return
  
  if (show) {
    // 隐藏行政区划填充，避免干扰热力图
    mapRef.value?.setDistrictStyle({ fillOpacity: 0, color: '#999', weight: 1 })

    if (heatmapLayer) return

    let heatData = []
    
    // 优先使用API返回的真实/模拟热力点
    if (populationData.value.heatmap_points && populationData.value.heatmap_points.length > 0) {
       heatData = populationData.value.heatmap_points
    } else {
      // 降级策略
      // ... (code omitted for brevity, logic remains same)
      const districts = populationData.value.districts || []
      districts.forEach(district => {
         const center = districtCenters[district.name]
         if (center) {
           const count = Math.floor((district.population_density || 500) / 5)
           for (let i = 0; i < count; i++) {
             heatData.push([
               center[0] + (Math.random() - 0.5) * 0.1,
               center[1] + (Math.random() - 0.5) * 0.1,
               Math.random()
             ])
           }
         }
      })
    }

    heatmapLayer = L.heatLayer(heatData, {
      radius: 15, // 调小半径，以显示基于真实小区的分布纹理
      blur: 20,   // 降低模糊，保留颗粒感和不规则边界
      maxZoom: 13,
      max: 0.6,
      minOpacity: 0.05,
      gradient: {
        0.2: '#6a1b9a', // 深紫色 (更接近图二背景)
        0.4: '#2196f3', // 蓝色
        0.6: '#00e676', // 绿色
        0.8: '#ffeb3b', // 黄色
        1.0: '#d50000'  // 深红
      }
    }).addTo(map)
  } else {
    // 恢复行政区划样式
    mapRef.value?.setDistrictStyle({ color: '#C41E3A', weight: 2, fillColor: '#C41E3A', fillOpacity: 0.1 })
    
    if (heatmapLayer) {
      map.removeLayer(heatmapLayer)
      heatmapLayer = null
    }
  }
}

</script>

<style scoped>
.population-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

.map-legend {
  position: absolute;
  bottom: 24px;
  left: 16px;
  width: 200px;
  z-index: 500;
}

.gradient-bar {
  height: 16px;
  background: linear-gradient(90deg, #fee08b, #fdae61, #f46d43, #d73027, #a50026);
  border-radius: 4px;
  margin-bottom: 4px;
}

.gradient-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-muted);
}

.analysis-panel {
  width: 360px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.overview-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.overview-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: center;
}

.overview-card .card-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--mazu-red-light), var(--golden));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.overview-card .card-label {
  font-size: 12px;
  color: var(--text-muted);
}

.chart-section h4,
.ranking-section h4,
.selected-detail h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.chart-section h4::before,
.ranking-section h4::before,
.selected-detail h4::before {
  content: '';
  width: 3px;
  height: 14px;
  background: var(--mazu-red);
  border-radius: 2px;
}

.chart-container {
  height: 200px;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.ranking-item:hover {
  background: var(--bg-card-hover);
}

.ranking-item .rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.ranking-item .rank.top {
  background: linear-gradient(135deg, var(--mazu-red), var(--golden));
  color: white;
}

.ranking-item .name {
  flex: 1;
  font-size: 13px;
}

.ranking-item .value {
  font-size: 12px;
  color: var(--golden);
}

.selected-detail {
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--mazu-red);
  border-radius: var(--radius-md);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.detail-item {
  text-align: center;
}

.detail-item .label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.detail-item .value {
  font-size: 14px;
  font-weight: 600;
  color: var(--golden);
}
</style>
