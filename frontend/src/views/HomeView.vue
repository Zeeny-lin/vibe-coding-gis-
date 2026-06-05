<template>
  <div class="home-view">
    <!-- 地图区域 -->
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="poiData"
        @featureClick="handleFeatureClick"
      />

      <!-- 信息面板叠加层 -->
      <div class="info-overlay">
        <!-- 城市概况卡片 -->
        <div class="city-card panel">
          <div class="city-header">
            <h2>🌊 莆田市</h2>
            <span class="subtitle">妈祖故里 · 进士之乡</span>
          </div>
          <div class="city-stats">
            <div class="stat-item">
              <span class="stat-value">{{ cityData.population }}</span>
              <span class="stat-label">常住人口(万)</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ cityData.gdp }}</span>
              <span class="stat-label">GDP(亿元)</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ cityData.area }}</span>
              <span class="stat-label">面积(km²)</span>
            </div>
          </div>
        </div>

        <!-- 图例面板 -->
        <div class="legend-panel panel">
          <div class="panel-header">
            <span class="panel-title">图例</span>
          </div>
          <div class="legend-items">
            <div class="legend-item" v-for="item in legendItems" :key="item.type">
              <span class="legend-dot" :style="{ background: item.color }"></span>
              <span>{{ item.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 区县信息弹出面板 -->
      <transition name="slide">
        <div class="district-detail-panel panel" v-if="selectedDistrict">
          <div class="panel-header">
            <span class="panel-title">{{ selectedDistrict.name }}</span>
            <el-button 
              :icon="Close" 
              circle 
              size="small" 
              @click="selectedDistrict = null"
            />
          </div>
          <div class="detail-content">
            <div class="detail-row">
              <span class="label">人口</span>
              <span class="value">{{ selectedDistrict.population }} 万</span>
            </div>
            <div class="detail-row">
              <span class="label">面积</span>
              <span class="value">{{ selectedDistrict.area }} km²</span>
            </div>
            <div class="detail-row">
              <span class="label">GDP</span>
              <span class="value">{{ selectedDistrict.gdp }} 亿元</span>
            </div>
            <div class="detail-row">
              <span class="label">城镇化率</span>
              <span class="value">{{ selectedDistrict.urban_rate }}%</span>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 底部统计栏 -->
    <div class="stats-bar">
      <div class="stat-card" v-for="stat in quickStats" :key="stat.label">
        <el-icon :size="24" :style="{ color: stat.color }">
          <component :is="stat.icon" />
        </el-icon>
        <div class="stat-info">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Close, User, TrendCharts, Place, OfficeBuilding, School } from '@element-plus/icons-vue'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

const mapRef = ref(null)
const districtsData = ref(null)
const poiData = ref(null)
const statisticsData = ref(null)
const selectedDistrict = ref(null)

// 城市概况数据
const cityData = computed(() => ({
  population: statisticsData.value?.total_population || 306.8,
  gdp: statisticsData.value?.total_gdp || 2880.5,
  area: 4200
}))

// 快速统计
const quickStats = computed(() => [
  { label: '行政区划', value: '4区1县', icon: Place, color: '#C41E3A' },
  { label: '常住人口', value: `${cityData.value.population}万`, icon: User, color: '#FFD700' },
  { label: 'GDP总量', value: `${cityData.value.gdp}亿`, icon: TrendCharts, color: '#00A8E8' },
  { label: '妈祖庙宇', value: '5座', icon: OfficeBuilding, color: '#C41E3A' },
  { label: '中小学校', value: '263所', icon: School, color: '#00C853' }
])

// 图例配置
const legendItems = [
  { type: 'district', label: '行政区划', color: '#C41E3A' },
  { type: 'mazu', label: '妈祖文化', color: '#C41E3A' },
  { type: 'hospital', label: '医疗机构', color: '#00A8E8' },
  { type: 'school', label: '教育机构', color: '#00C853' },
  { type: 'scenic', label: '风景名胜', color: '#FFD700' }
]

// 加载数据
onMounted(async () => {
  try {
    // 加载行政区划
    const districts = await api.getDistricts()
    districtsData.value = districts

    // 加载POI
    const poi = await api.getPOI()
    poiData.value = poi

    // 加载统计数据
    const stats = await api.getStatistics()
    statisticsData.value = stats
  } catch (error) {
    console.error('数据加载失败:', error)
  }
})

// 处理区域点击
const handleFeatureClick = async (properties) => {
  try {
    const stats = await api.getDistrictStats(properties.name)
    selectedDistrict.value = {
      ...properties,
      ...stats.district
    }
  } catch (error) {
    selectedDistrict.value = properties
  }
}
</script>

<style scoped>
.home-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.map-section {
  flex: 1;
  position: relative;
}

.info-overlay {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 500;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 城市概况卡片 */
.city-card {
  width: 260px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
}

.city-header {
  margin-bottom: 16px;
}

.city-header h2 {
  font-size: 20px;
  margin-bottom: 4px;
  background: linear-gradient(135deg, var(--mazu-red-light), var(--golden));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.city-header .subtitle {
  font-size: 12px;
  color: var(--text-secondary);
}

.city-stats {
  display: flex;
  justify-content: space-between;
}

.stat-item {
  text-align: center;
}

.stat-item .stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--golden);
}

.stat-item .stat-label {
  font-size: 11px;
  color: var(--text-muted);
}

/* 图例面板 */
.legend-panel {
  width: 160px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

/* 区县详情面板 */
.district-detail-panel {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 280px;
  z-index: 500;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.detail-row .label {
  color: var(--text-secondary);
  font-size: 13px;
}

.detail-row .value {
  color: var(--golden);
  font-weight: 600;
}

/* 底部统计栏 */
.stats-bar {
  height: 80px;
  background: var(--bg-darker);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0 32px;
}

.stats-bar .stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.stats-bar .stat-info {
  display: flex;
  flex-direction: column;
}

.stats-bar .stat-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.stats-bar .stat-label {
  font-size: 11px;
  color: var(--text-muted);
}

/* 动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
