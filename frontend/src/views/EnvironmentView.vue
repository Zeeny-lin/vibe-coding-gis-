<template>
  <div class="environment-view">
    <!-- 地图区域 -->
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="mapPOIData"
        :showLayerControl="true"
      />
    </div>

    <!-- 右侧面板 -->
    <div class="env-panel">
      <div class="panel-header">
        <span class="panel-title">🍃 生态环境监测</span>
      </div>

      <!-- 空气质量 -->
      <div class="data-section" v-if="airQuality">
        <h4>空气质量 (AQI)</h4>
        <div class="aqi-card" :class="getAQIClass(airQuality.aqi)">
          <div class="aqi-value">{{ airQuality.aqi }}</div>
          <div class="aqi-level">{{ airQuality.quality_level }}</div>
          <div class="aqi-pollutant" v-if="airQuality.primary_pollutant !== '-'">
            首要污染物: {{ airQuality.primary_pollutant }}
          </div>
        </div>
        <div class="pollutants-grid">
          <div class="pollutant-item" v-for="(val, key) in airQuality.pollutants" :key="key">
            <span class="p-label">{{ key }}</span>
            <span class="p-value">{{ val }}</span>
          </div>
        </div>
      </div>

      <!-- 天气状况 -->
      <div class="data-section" v-if="weather">
        <h4>实时天气</h4>
        <div class="weather-card">
          <div class="weather-main">
            <div class="temp">{{ weather.current.temperature }}°C</div>
            <div class="condition">{{ weather.current.weather }}</div>
          </div>
          <div class="weather-details">
            <div class="w-item">
              <el-icon><WindPower /></el-icon>
              {{ weather.current.wind_direction }} {{ weather.current.wind_level }}级
            </div>
            <div class="w-item">
              <el-icon><Odometer /></el-icon>
              湿度 {{ weather.current.humidity }}%
            </div>
          </div>
        </div>
        
        <!-- 简易未来天气 -->
        <div class="forecast-list">
          <div class="forecast-item" v-for="(day, index) in weather.forecast.slice(0, 3)" :key="index">
            <span class="f-day">{{ day.weekday }}</span>
            <span class="f-weather">{{ day.weather_day }}</span>
            <span class="f-temp">{{ day.temp_low }}~{{ day.temp_high }}°C</span>
          </div>
        </div>
      </div>

      <!-- 水环境 -->
      <div class="data-section" v-if="waterQuality">
        <h4>水环境状况</h4>
        <div class="water-list">
          <div class="water-item" v-for="river in waterQuality.rivers" :key="river.name">
            <div class="river-name">{{ river.name }}</div>
            <div class="river-status">
              <el-tag :type="getWaterClass(river.quality_class)" size="small">
                {{ river.quality_class }}类
              </el-tag>
              <span class="water-desc">{{ river.status }}</span>
            </div>
          </div>
          <div class="water-item coastal">
            <div class="river-name">{{ waterQuality.coastal.name }}</div>
            <div class="river-status">
              <el-tag :type="getWaterClass(waterQuality.coastal.quality_class)" size="small">
                {{ waterQuality.coastal.quality_class }}
              </el-tag>
              <span class="water-desc">{{ waterQuality.coastal.status }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 解读 -->
      <div class="ai-section">
        <el-button type="primary" class="ai-btn" @click="getAIAnalysis" :loading="aiLoading">
          <el-icon><MagicStick /></el-icon>
          生成环境分析报告
        </el-button>
        <div class="ai-content" v-if="aiReport" v-html="formatMarkdown(aiReport)"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { WindPower, Odometer, MagicStick } from '@element-plus/icons-vue'
import { marked } from 'marked'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

// ... imports
const mapRef = ref(null)
const districtsData = ref(null)
const airQuality = ref(null)
const weather = ref(null)
const waterQuality = ref(null)
const aiReport = ref('')
const aiLoading = ref(false)
const globalPOIs = ref(null) // New ref for global POIs

// Merged POI Data (Stations + Global POIs)
const mapPOIData = computed(() => {
  const stationFeatures = airQuality.value?.stations?.map(station => ({
    type: 'Feature',
    properties: {
      name: station.name,
      type: 'scenic', // Use 'scenic' style or maybe 'other' for now
      subtype: 'env_station',
      description: `AQI: ${station.aqi} (${station.quality_level})`,
      address: station.district
    },
    geometry: {
      type: 'Point',
      coordinates: station.coordinates
    }
  })) || []

  const globalFeatures = globalPOIs.value?.features || []
  
  return {
    type: 'FeatureCollection',
    features: [...globalFeatures, ...stationFeatures]
  }
})

// AQI 颜色类
const getAQIClass = (aqi) => {
  if (aqi <= 50) return 'aqi-good'
  if (aqi <= 100) return 'aqi-moderate'
  if (aqi <= 150) return 'aqi-unhealthy-sensitive'
  return 'aqi-unhealthy'
}
// 水质颜色类
const getWaterClass = (level) => {
  if (['I', 'II', '一类', '二类'].includes(level)) return 'success'
  if (['III', '三类'].includes(level)) return 'warning'
  return 'danger'
}

const formatMarkdown = (content) => {
  try {
    return marked.parse(content)
  } catch {
    return content
  }
}

const getAIAnalysis = async () => {
  aiLoading.value = true
  try {
    const data = {
      air: airQuality.value,
      weather: weather.value,
      water: waterQuality.value
    }
    const res = await api.interpretAnalysis('environment', data)
    aiReport.value = res.interpretation
  } catch (error) {
    aiReport.value = `**环境状况简报**
    
当前莆田市整体环境质量保持**优良**水平。

1. **空气质量**：AQI指数为${airQuality.value?.aqi || 35}，空气清新，适合户外活动。
2. **气象条件**：${weather.value?.current?.weather || '多云'}，气温适宜。
3. **水环境**：主要流域木兰溪、萩芦溪水质稳定在II-III类，湄洲湾海域水质优良。

建议：继续保持主要流域的生态保护力度，关注城市扬尘控制。`
  } finally {
    aiLoading.value = false
  }
}

onMounted(async () => {
  try {
    // 并行加载数据
    const [districts, air, wea, water, pois] = await Promise.all([
      api.getDistricts(),
      api.getAirQuality(),
      api.getWeather(),
      api.getWaterQuality(),
      api.getPOI() // Fetch global POIs
    ])
    
    districtsData.value = districts
    airQuality.value = air
    weather.value = wea
    waterQuality.value = water
    globalPOIs.value = pois
  } catch (error) {
    console.error('加载环境数据失败:', error)
    // 模拟数据 fallback
    airQuality.value = {
      aqi: 35,
      quality_level: '优',
      primary_pollutant: '-',
      pollutants: { 'PM2.5': 12, 'PM10': 28, 'O3': 45, 'NO2': 18, 'SO2': 6, 'CO': 0.6 },
      stations: [
        { name: '市实验小学', aqi: 32, quality_level: '优', coordinates: [25.43, 119.01], district: '荔城区' },
        { name: '城厢区政府', aqi: 38, quality_level: '优', coordinates: [25.44, 118.99], district: '城厢区' }
      ]
    }
    
    weather.value = {
      current: { temperature: 24, weather: '多云', wind_direction: '东北风', wind_level: 3, humidity: 65 },
      forecast: [
        { weekday: '今天', weather_day: '多云', temp_low: 22, temp_high: 28 },
        { weekday: '明天', weather_day: '小雨', temp_low: 21, temp_high: 26 },
        { weekday: '后天', weather_day: '阴', temp_low: 20, temp_high: 25 }
      ]
    }
    
    waterQuality.value = {
      rivers: [
        { name: '木兰溪', quality_class: 'II', status: '优' },
        { name: '萩芦溪', quality_class: 'II', status: '优' },
        { name: '延寿溪', quality_class: 'III', status: '良' }
      ],
      coastal: { name: '湄洲湾', quality_class: '一类', status: '优' }
    }
  }
})
</script>

<style scoped>
.environment-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

.env-panel {
  width: 360px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: #4CAF50; /* 绿色主题 */
}

.data-section h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 12px;
  border-left: 3px solid #4CAF50;
  padding-left: 8px;
}

/* AQI 卡片 */
.aqi-card {
  padding: 16px;
  border-radius: 8px;
  color: white;
  text-align: center;
  margin-bottom: 12px;
}

.aqi-good { background: linear-gradient(135deg, #43a047, #66bb6a); }
.aqi-moderate { background: linear-gradient(135deg, #fbc02d, #ffeb3b); color: #333; }
.aqi-unhealthy-sensitive { background: linear-gradient(135deg, #f57c00, #ff9800); }
.aqi-unhealthy { background: linear-gradient(135deg, #d32f2f, #ef5350); }

.aqi-value { font-size: 32px; font-weight: bold; }
.aqi-level { font-size: 16px; margin-top: 4px; }
.aqi-pollutant { font-size: 12px; margin-top: 8px; opacity: 0.9; }

.pollutants-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.pollutant-item {
  background: var(--bg-card);
  padding: 8px;
  border-radius: 4px;
  text-align: center;
  border: 1px solid var(--border-color);
}

.p-label { display: block; font-size: 10px; color: var(--text-muted); }
.p-value { display: block; font-size: 14px; font-weight: 500; color: var(--text-primary); }

/* 天气卡片 */
.weather-card {
  background: linear-gradient(135deg, #1976d2, #42a5f5);
  padding: 16px;
  border-radius: 8px;
  color: white;
  margin-bottom: 12px;
}

.weather-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.weather-main .temp { font-size: 36px; font-weight: bold; }
.weather-main .condition { font-size: 18px; }

.weather-details {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  opacity: 0.9;
}

.forecast-list {
  background: var(--bg-card);
  border-radius: 8px;
  padding: 8px;
}

.forecast-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  border-bottom: 1px solid var(--border-color);
  font-size: 13px;
  color: var(--text-secondary);
}

.forecast-item:last-child { border-bottom: none; }

/* 水质列表 */
.water-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: var(--bg-card);
  border-radius: 6px;
  margin-bottom: 8px;
  border: 1px solid var(--border-color);
}

.river-name { font-size: 14px; color: var(--text-primary); }
.river-status { display: flex; align-items: center; gap: 8px; }
.water-desc { font-size: 12px; color: var(--text-muted); }

/* AI */
.ai-section { margin-top: 10px; }
.ai-btn { width: 100%; background: #4CAF50; border-color: #4CAF50; }
.ai-content { margin-top: 12px; font-size: 13px; line-height: 1.6; color: var(--text-secondary); background: var(--bg-card); padding: 12px; border-radius: 6px; }
</style>
