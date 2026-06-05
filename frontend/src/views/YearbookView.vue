<template>
  <div class="yearbook-view">
    <div class="page-header">
      <h2>📊 统计年鉴</h2>
      <p class="subtitle">莆田市2019-2025年主要经济社会指标</p>
      <a :href="sourceUrl" target="_blank" class="source-link">数据来源: 莆田市统计年鉴 →</a>
    </div>

    <div class="charts-grid" v-loading="loading">
      <!-- GDP趋势图 -->
      <div class="chart-card">
        <h3>📈 地区生产总值(GDP)</h3>
        <div ref="gdpChartRef" class="chart-container"></div>
      </div>

      <!-- 人口变化图 -->
      <div class="chart-card">
        <h3>👥 常住人口与城镇化率</h3>
        <div ref="populationChartRef" class="chart-container"></div>
      </div>

      <!-- 居民收入对比图 -->
      <div class="chart-card">
        <h3>💰 城乡居民人均可支配收入</h3>
        <div ref="incomeChartRef" class="chart-container"></div>
      </div>

      <!-- 产业结构图 -->
      <div class="chart-card">
        <h3>🏭 三次产业结构变化</h3>
        <div ref="industryChartRef" class="chart-container"></div>
      </div>

      <!-- 各区县GDP饼图 -->
      <div class="chart-card">
        <h3>🗺️ {{ currentYear }}年各区县GDP分布</h3>
        <div ref="districtChartRef" class="chart-container"></div>
      </div>

      <!-- 主要指标表格 -->
      <div class="chart-card wide">
        <h3>📋 {{ currentYear }}年主要指标一览(含预计)</h3>
        <div class="stats-table">
          <div class="stat-row" v-for="(stat, key) in summaryStats" :key="key">
            <span class="stat-label">{{ stat.name }}</span>
            <span class="stat-value">{{ stat.value }} <small>{{ stat.unit }}</small></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '@/services/api'

const loading = ref(true)
const sourceUrl = ref('https://www.putian.gov.cn/zjpt/pttjnj/')
const yearbookData = ref(null)
const summaryStats = ref({})
const currentYear = ref('2024')

// 图表DOM引用
const gdpChartRef = ref(null)
const populationChartRef = ref(null)
const incomeChartRef = ref(null)
const industryChartRef = ref(null)
const districtChartRef = ref(null)

// 图表实例
let gdpChart = null
let populationChart = null
let incomeChart = null
let industryChart = null
let districtChart = null

// 初始化GDP图表
const initGdpChart = () => {
  if (!gdpChartRef.value || !yearbookData.value) return
  
  gdpChart = echarts.init(gdpChartRef.value)
  const data = yearbookData.value
  
  gdpChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['GDP总量', 'GDP增速'],
      textStyle: { color: '#ccc' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.years,
      axisLabel: { color: '#ccc' }
    },
    yAxis: [
      {
        type: 'value',
        name: '亿元',
        axisLabel: { color: '#ccc' },
        splitLine: { lineStyle: { color: '#333' } }
      },
      {
        type: 'value',
        name: '%',
        axisLabel: { color: '#ccc' },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: 'GDP总量',
        type: 'bar',
        data: data.gdp.values,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' }
          ])
        }
      },
      {
        name: 'GDP增速',
        type: 'line',
        yAxisIndex: 1,
        data: data.gdpGrowth.values,
        smooth: true,
        lineStyle: { color: '#00C853', width: 3 },
        itemStyle: { color: '#00C853' }
      }
    ]
  })
}

// 初始化人口图表
const initPopulationChart = () => {
  if (!populationChartRef.value || !yearbookData.value) return
  
  populationChart = echarts.init(populationChartRef.value)
  const data = yearbookData.value
  
  populationChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['常住人口', '城镇化率'],
      textStyle: { color: '#666' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.years,
      axisLabel: { color: '#666' }
    },
    yAxis: [
      {
        type: 'value',
        name: '万人',
        min: 280,
        axisLabel: { color: '#666' },
        splitLine: { lineStyle: { color: '#eee' } }
      },
      {
        type: 'value',
        name: '%',
        min: 50,
        max: 70,
        axisLabel: { color: '#666' },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '常住人口',
        type: 'bar',
        data: data.population.values,
        itemStyle: { color: '#00BCD4' }
      },
      {
        name: '城镇化率',
        type: 'line',
        yAxisIndex: 1,
        data: data.urbanPopulationRate.values,
        smooth: true,
        areaStyle: { opacity: 0.3 },
        lineStyle: { color: '#FF9800', width: 3 },
        itemStyle: { color: '#FF9800' }
      }
    ]
  })
}

// 初始化收入图表
const initIncomeChart = () => {
  if (!incomeChartRef.value || !yearbookData.value) return
  
  incomeChart = echarts.init(incomeChartRef.value)
  const data = yearbookData.value
  
  incomeChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['城镇居民', '农村居民'],
      textStyle: { color: '#666' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.years,
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      name: '元',
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#eee' } }
    },
    series: [
      {
        name: '城镇居民',
        type: 'line',
        data: data.urbanIncome.values,
        smooth: true,
        areaStyle: { opacity: 0.2 },
        lineStyle: { color: '#E91E63', width: 3 },
        itemStyle: { color: '#E91E63' }
      },
      {
        name: '农村居民',
        type: 'line',
        data: data.ruralIncome.values,
        smooth: true,
        areaStyle: { opacity: 0.2 },
        lineStyle: { color: '#4CAF50', width: 3 },
        itemStyle: { color: '#4CAF50' }
      }
    ]
  })
}

// 初始化产业结构图表
const initIndustryChart = () => {
  if (!industryChartRef.value || !yearbookData.value) return
  
  industryChart = echarts.init(industryChartRef.value)
  const data = yearbookData.value.industryStructure
  
  industryChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['第一产业', '第二产业', '第三产业'],
      textStyle: { color: '#666' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.years,
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      name: '%',
      max: 100,
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#eee' } }
    },
    series: [
      {
        name: '第一产业',
        type: 'bar',
        stack: 'total',
        data: data.primary,
        itemStyle: { color: '#8BC34A' }
      },
      {
        name: '第二产业',
        type: 'bar',
        stack: 'total',
        data: data.secondary,
        itemStyle: { color: '#2196F3' }
      },
      {
        name: '第三产业',
        type: 'bar',
        stack: 'total',
        data: data.tertiary,
        itemStyle: { color: '#FF5722' }
      }
    ]
  })
}

// 初始化区县GDP饼图
const initDistrictChart = () => {
  if (!districtChartRef.value || !yearbookData.value) return
  
  districtChart = echarts.init(districtChartRef.value)
  const data = yearbookData.value.districtGDP2024 || yearbookData.value.districtGDP2023 || yearbookData.value.districtGDP
  
  const pieData = data.districts.map((name, i) => ({
    name,
    value: data.values[i]
  }))
  
  districtChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}亿元 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#666' }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#1a1a2e',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            color: '#fff'
          }
        },
        data: pieData,
        color: ['#667eea', '#764ba2', '#00BCD4', '#FF9800', '#E91E63']
      }
    ]
  })
}

// 准备汇总统计
const prepareSummaryStats = () => {
  const data = yearbookData.value
  // 获取倒数第二个索引（2024年），因为2025是预测值，我们优先显示2024实际值，或者如果有2025也行
  // 这里我们去除非空值的最后一个有效数据
  const lastIndex = data.years.length - 2 // 2024年 (index 5, length 7)
  
  // 更新当前显示年份
  currentYear.value = data.years[lastIndex]
  
  summaryStats.value = {
    gdp: { name: '地区生产总值', value: data.gdp.values[lastIndex], unit: '亿元' },
    population: { name: '常住人口', value: data.population.values[lastIndex], unit: '万人' },
    perCapitaGDP: { name: '人均GDP', value: (data.perCapitaGDP.values[lastIndex] / 10000).toFixed(1), unit: '万元' },
    urbanIncome: { name: '城镇居民收入', value: data.urbanIncome.values[lastIndex], unit: '元' },
    fiscal: { name: '财政总收入', value: data.fiscalRevenue.values[lastIndex], unit: '亿元' },
    tourism: { name: '旅游总收入', value: data.tourism.values[lastIndex], unit: '亿元' }
  }
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  gdpChart?.resize()
  populationChart?.resize()
  incomeChart?.resize()
  industryChart?.resize()
  districtChart?.resize()
}

onMounted(async () => {
  try {
    yearbookData.value = await api.getYearbook()
    loading.value = false
    
    await nextTick()
    
    initGdpChart()
    initPopulationChart()
    initIncomeChart()
    initIndustryChart()
    initDistrictChart()
    prepareSummaryStats()
    
    window.addEventListener('resize', handleResize)
  } catch (error) {
    console.error('加载年鉴数据失败:', error)
    loading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  gdpChart?.dispose()
  populationChart?.dispose()
  incomeChart?.dispose()
  industryChart?.dispose()
  districtChart?.dispose()
})
</script>

<style scoped>
.yearbook-view {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
  /* background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);  Remove hardcoded dark gradient */
  background: transparent;
}

.page-header {
  margin-bottom: 28px;
  text-align: center;
}

.page-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 12px 0 8px;
  color: var(--text-secondary);
  font-size: 15px;
}

.source-link {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 20px;
  color: #667eea;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s;
}

.source-link:hover {
  background: rgba(102, 126, 234, 0.25);
  transform: translateY(-2px);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding-bottom: 40px;
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s, box-shadow 0.3s;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--mazu-red);
}

.chart-card.wide {
  grid-column: span 2;
}

.chart-card h3 {
  margin: 0 0 20px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.chart-container {
  height: 300px;
}

/* 统计表格 - 更精致的设计 */
.stats-table {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-row {
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: center;
  transition: all 0.3s;
}

.stat-row:hover {
  background: #fff;
  box-shadow: var(--shadow-md);
  transform: scale(1.02);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-value small {
  font-size: 14px;
  font-weight: normal;
  -webkit-text-fill-color: var(--text-muted);
}

/* 响应式 */
@media (max-width: 1400px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-card.wide {
    grid-column: span 1;
  }
  
  .stats-table {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-table {
    grid-template-columns: 1fr;
  }
}
</style>
