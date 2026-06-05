<template>
  <div class="economy-view">
    <!-- 左侧地图区域 -->
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="poiData"
        :showLayerControl="true"
      />
    </div>

    <!-- 右侧分析面板 -->
    <div class="analysis-panel">
      <div class="panel-header">
        <span class="panel-title">经济产业分析</span>
      </div>

      <!-- GDP总量概况 -->
      <div class="overview-section">
        <div class="overview-card highlight">
          <span class="card-value">{{ economyData.total_gdp || '-' }}</span>
          <span class="card-label">GDP总量(亿元)</span>
          <span class="card-growth" v-if="economyData.gdp_growth">
            <el-icon><Top /></el-icon> {{ economyData.gdp_growth }}%
          </span>
        </div>
        <div class="overview-card">
          <span class="card-value">{{ formatMoney(economyData.gdp_per_capita) }}</span>
          <span class="card-label">人均GDP(元)</span>
        </div>
      </div>
      
      <!-- 重点产业链图表 (新增) -->
      <div class="chart-section wide">
        <h4>12条重点产业链产值 (亿元)</h4>
        <div ref="keyIndustryChartRef" class="chart-container" style="height: 250px;"></div>
      </div>

      <!-- GDP分布图表 -->
      <div class="chart-section">
        <h4>各区县GDP分布</h4>
        <div ref="gdpChartRef" class="chart-container"></div>
      </div>

      <!-- 产业结构图表 -->
      <div class="chart-section">
        <h4>产业结构对比</h4>
        <div ref="industryChartRef" class="chart-container"></div>
      </div>

      <!-- GDP人均排名 -->
      <div class="ranking-section">
        <h4>人均GDP排名</h4>
        <div class="ranking-list">
          <div 
            class="ranking-item" 
            v-for="(district, index) in sortedByGdpPerCapita" 
            :key="district.name"
          >
            <span class="rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
            <span class="name">{{ district.name }}</span>
            <span class="value">{{ formatMoney(district.gdp_per_capita) }} 元</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { Top } from '@element-plus/icons-vue' // 需要导入图标
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

const mapRef = ref(null)
const gdpChartRef = ref(null)
const industryChartRef = ref(null)
const keyIndustryChartRef = ref(null) // 新增引用
const districtsData = ref(null)
const poiData = ref(null) // POI数据
const economyData = ref({})
let gdpChart = null
let industryChart = null
let keyIndustryChart = null

// 按人均GDP排序
const sortedByGdpPerCapita = computed(() => {
  const districts = economyData.value.districts || []
  return [...districts].sort((a, b) => (b.gdp_per_capita || 0) - (a.gdp_per_capita || 0))
})

// 格式化金额
const formatMoney = (value) => {
  if (!value) return '0'
  return value.toLocaleString()
}

// 初始化GDP图表
const initGdpChart = () => {
  if (!gdpChartRef.value) return
  
  gdpChart = echarts.init(gdpChartRef.value)
  
  const districts = economyData.value.districts || []
  const data = districts.map(d => ({
    name: d.name,
    value: d.gdp
  }))

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}亿元 ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 0,
      textStyle: { color: '#a0a0b0', fontSize: 11 }
    },
    series: [{
      name: 'GDP',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#1a1a2e',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold',
          color: '#fff'
        }
      },
      data: data,
      color: ['#C41E3A', '#E8425A', '#FFD700', '#00A8E8', '#00C853']
    }]
  }

  gdpChart.setOption(option)
}

// 初始化产业结构图表
const initIndustryChart = () => {
  if (!industryChartRef.value) return
  
  industryChart = echarts.init(industryChartRef.value)
  
  const districts = economyData.value.districts || []
  const names = districts.map(d => d.name)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['第一产业', '第二产业', '第三产业'],
      textStyle: { color: '#a0a0b0', fontSize: 11 },
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0', fontSize: 10, rotate: 15 }
    },
    yAxis: {
      type: 'value',
      name: '亿元',
      nameTextStyle: { color: '#a0a0b0' },
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0' },
      splitLine: { lineStyle: { color: '#2a2a4a' } }
    },
    series: [
      {
        name: '第一产业',
        type: 'bar',
        stack: 'total',
        data: districts.map(d => d.primary_industry),
        itemStyle: { color: '#00C853' }
      },
      {
        name: '第二产业',
        type: 'bar',
        stack: 'total',
        data: districts.map(d => d.secondary_industry),
        itemStyle: { color: '#00A8E8' }
      },
      {
        name: '第三产业',
        type: 'bar',
        stack: 'total',
        data: districts.map(d => d.tertiary_industry),
        itemStyle: { color: '#C41E3A' }
      }
    ]
  }

  industryChart.setOption(option)
}

// 初始化重点产业链图表 (新增)
const initKeyIndustryChart = () => {
  if (!keyIndustryChartRef.value) return
  
  keyIndustryChart = echarts.init(keyIndustryChartRef.value)
  
  const industries = economyData.value.key_industries || []
  // 按产值排序
  industries.sort((a, b) => a.value - b.value)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: '{b}<br/>产值: {c} 亿元<br/>增速: {data.growth}%'
    },
    grid: { left: '3%', right: '10%', bottom: '3%', top: '2%', containLabel: true },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#eee' } }
    },
    yAxis: {
      type: 'category',
      data: industries.map(i => i.name),
      axisLabel: { color: '#2c3e50', fontWeight: 'bold' },
      axisLine: { lineStyle: { color: '#ddd' } },
      axisTick: { show: false }
    },
    series: [
      {
        name: '产值',
        type: 'bar',
        data: industries.map(i => ({ value: i.value, growth: i.growth })),
        label: {
          show: true,
          position: 'right',
          color: '#666',
          formatter: '{c} 亿'
        },
        itemStyle: {
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#C41E3A' }, // 妈祖红
            { offset: 1, color: '#FFD700' }  // 金色
          ]),
          borderRadius: [0, 4, 4, 0]
        }
      }
    ]
  }
  
  keyIndustryChart.setOption(option)
}

// 加载数据
onMounted(async () => {
  try {
    // 加载行政区划
    const districts = await api.getDistricts()
    districtsData.value = districts

    // 加载经济统计
    const economy = await api.getEconomyStats()
    economyData.value = economy

    await nextTick()
    initGdpChart()
    initIndustryChart()
    initKeyIndustryChart()
  } catch (error) {
    console.error('数据加载失败:', error)
    // 简单Fallback防止页面崩溃
    economyData.value = { total_gdp: '-', districts: [] }
  }

  // POI单独加载，失败不影响主数据
  try {
    const pois = await api.getPOI()
    poiData.value = pois
  } catch (e) {
    console.warn('POI加载失败:', e)
  }
})
</script>

<style scoped>
.economy-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

.analysis-panel {
  width: 480px;
  min-width: 480px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.overview-section {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.overview-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  text-align: center;
  width: 100%;
}

.overview-card.highlight {
  background: linear-gradient(135deg, rgba(196, 30, 58, 0.2), rgba(255, 215, 0, 0.1));
  border-color: var(--mazu-red);
}

.overview-card .card-value {
  display: block;
  font-size: 42px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--mazu-red-light), var(--golden));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.overview-card .card-label {
  display: block;
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.overview-card .card-growth {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  margin-top: 8px;
  font-size: 13px;
  color: #f56c6c;
  font-weight: 600;
  background: rgba(245, 108, 108, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
}

.chart-section h4,
.ranking-section h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.chart-section h4::before,
.ranking-section h4::before {
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
  font-weight: 500;
}
</style>
