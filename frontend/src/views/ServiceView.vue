<template>
  <div class="service-view">
    <!-- 地图区域 -->
    <div class="map-section">
      <MapView 
        ref="mapRef"
        :geojsonData="districtsData"
        :poiData="servicePOI"
        :showLayerControl="false"
      />
    </div>

    <!-- 右侧分析面板 -->
    <div class="analysis-panel">
      <div class="panel-header">
        <span class="panel-title">公共服务分析</span>
      </div>

      <!-- 服务类型选择 -->
      <div class="service-selector">
        <el-radio-group v-model="selectedServiceType" @change="analyzeService">
          <el-radio-button value="hospital">
            <el-icon><FirstAidKit /></el-icon>
            医疗
          </el-radio-button>
          <el-radio-button value="school">
            <el-icon><School /></el-icon>
            教育
          </el-radio-button>
          <el-radio-button value="housing">
            <el-icon><House /></el-icon>
            住房
          </el-radio-button>
        </el-radio-group>
      </div>

      <!-- 资源统计 -->
      <div class="resource-stats">
        <div class="stat-card">
          <span class="stat-value">{{ resourceStats.total }}</span>
          <span class="stat-label">{{ getStatLabel(0) }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ resourceStats.average }}</span>
          <span class="stat-label">{{ getStatLabel(1) }}</span>
        </div>
      </div>

      <!-- 住房价格分析 -->
      <div class="housing-analysis" v-if="selectedServiceType === 'housing'">
        <h4>🏠 房价分析</h4>
        <div ref="priceChartRef" class="price-chart"></div>
        <div class="price-stats">
          <div class="price-stat-item" v-for="d in housingStats" :key="d.district">
            <span class="district">{{ d.district }}</span>
            <span class="price">{{ d.avgPrice }} 元/㎡</span>
            <span class="count">{{ d.count }}套</span>
          </div>
        </div>
      </div>

      <!-- 可达性分析结果 -->
      <div class="accessibility-section" v-if="accessibilityData">
        <h4>可达性评估</h4>
        <div class="overall-score">
          <div class="score-circle" :class="getScoreClass(accessibilityData.overall_score)">
            <span class="score">{{ accessibilityData.overall_score }}</span>
            <span class="label">总体评分</span>
          </div>
          <div class="score-desc">
            <span class="assessment">{{ accessibilityData.coverage_assessment }}</span>
            <p>基于各区县到最近{{ selectedServiceType === 'hospital' ? '医疗' : '教育' }}设施距离分析</p>
          </div>
        </div>

        <!-- 各区县评分 -->
        <div class="district-scores">
          <div 
            class="district-score-item" 
            v-for="district in accessibilityData.district_results" 
            :key="district.district"
          >
            <span class="name">{{ district.district }}</span>
            <div class="score-bar-wrapper">
              <div 
                class="score-bar" 
                :style="{ width: district.score + '%' }"
                :class="getScoreClass(district.score)"
              ></div>
            </div>
            <span class="score-text">{{ district.accessibility }}</span>
          </div>
        </div>
      </div>

      <!-- 资源分布表 -->
      <div class="resource-table-section">
        <h4>区县资源分布</h4>
        <el-table :data="resourceTableData" style="width: 100%" size="small">
          <el-table-column prop="name" label="区县" width="80" />
          <el-table-column 
            :prop="selectedServiceType === 'hospital' ? 'hospitals' : 'schools'" 
            :label="selectedServiceType === 'hospital' ? '机构数' : '学校数'" 
            width="70"
          />
          <el-table-column 
            :prop="selectedServiceType === 'hospital' ? 'hospital_beds' : 'students'" 
            :label="selectedServiceType === 'hospital' ? '床位数' : '学生数'" 
          />
          <el-table-column 
            :prop="selectedServiceType === 'hospital' ? 'beds_per_1000' : 'teachers'"
            :label="selectedServiceType === 'hospital' ? '床位/千人' : '教师数'"
          />
        </el-table>
      </div>

      <!-- AI解读 -->
      <div class="ai-section">
        <el-button 
          type="primary" 
          class="ai-btn"
          @click="getAIAnalysis"
          :loading="aiLoading"
        >
          <el-icon><DataAnalysis /></el-icon>
          AI智能解读
        </el-button>

        <div class="ai-result" v-if="aiAnalysis">
          <div class="ai-content" v-html="formatMarkdown(aiAnalysis)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { FirstAidKit, School, DataAnalysis, House } from '@element-plus/icons-vue'
import { marked } from 'marked'
import * as echarts from 'echarts'
import MapView from '@/components/MapView.vue'
import api from '@/services/api'

const mapRef = ref(null)
const priceChartRef = ref(null)
const districtsData = ref(null)
const servicePOI = ref(null)
const selectedServiceType = ref('hospital')
const accessibilityData = ref(null)
const resourceData = ref(null)
const aiAnalysis = ref('')
const aiLoading = ref(false)
const housingData = ref(null)
const housingStats = ref([])
let priceChart = null

// 资源统计
const resourceStats = computed(() => {
  if (selectedServiceType.value === 'housing') {
    const total = housingStats.value.reduce((s, d) => s + d.count, 0)
    const avgPrice = housingStats.value.length > 0
      ? Math.round(housingStats.value.reduce((s, d) => s + d.avgPrice * d.count, 0) / total)
      : 0
    return { total, average: avgPrice }
  }
  const districts = resourceData.value?.districts || []
  if (selectedServiceType.value === 'hospital') {
    const total = districts.reduce((sum, d) => sum + (d.hospitals || 0), 0)
    const avgBeds = districts.reduce((sum, d) => sum + (d.beds_per_1000 || 0), 0) / (districts.length || 1)
    return { total, average: avgBeds.toFixed(2) }
  } else {
    const total = districts.reduce((sum, d) => sum + (d.schools || 0), 0)
    const totalStudents = districts.reduce((sum, d) => sum + (d.students || 0), 0)
    const totalTeachers = districts.reduce((sum, d) => sum + (d.teachers || 0), 0)
    return { total, average: totalTeachers ? (totalStudents / totalTeachers).toFixed(1) : 0 }
  }
})

// 统计标签
const getStatLabel = (idx) => {
  const labels = {
    hospital: ['医疗机构总数', '床位/千人'],
    school: ['学校总数', '生师比'],
    housing: ['房源总数', '均价(元/㎡)']
  }
  return labels[selectedServiceType.value][idx]
}

// 资源表格数据
const resourceTableData = computed(() => {
  return resourceData.value?.districts || []
})

// 获取评分样式类
const getScoreClass = (score) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

// 格式化Markdown
const formatMarkdown = (content) => {
  try {
    return marked.parse(content)
  } catch {
    return content
  }
}

// 分析服务
const analyzeService = async () => {
  try {
    if (selectedServiceType.value === 'housing') {
      // 加载住房数据
      const poi = await api.getPOI('housing')
      servicePOI.value = poi
      
      // 统计各区价格
      const stats = {}
      poi?.features?.forEach(f => {
        const d = f.properties.district
        if (!stats[d]) stats[d] = { count: 0, totalPrice: 0 }
        stats[d].count++
        stats[d].totalPrice += f.properties.unit_price
      })
      housingStats.value = Object.entries(stats).map(([district, data]) => ({
        district,
        count: data.count,
        avgPrice: Math.round(data.totalPrice / data.count)
      })).sort((a, b) => b.avgPrice - a.avgPrice)
      
      await nextTick()
      initPriceChart()
      return
    }
    
    // 加载对应类型POI
    const poi = await api.getPOI(selectedServiceType.value)
    servicePOI.value = poi

    // 可达性分析
    const accessibility = await api.accessibilityAnalysis(selectedServiceType.value)
    accessibilityData.value = accessibility
    
    aiAnalysis.value = ''
  } catch (error) {
    console.error('分析失败:', error)
    // 使用模拟数据
    accessibilityData.value = {
      overall_score: selectedServiceType.value === 'hospital' ? 65 : 72,
      coverage_assessment: selectedServiceType.value === 'hospital' ? '需改善' : '均衡',
      district_results: [
        { district: '城厢区', score: 90, accessibility: '优秀', poi_count: 8 },
        { district: '荔城区', score: 85, accessibility: '优秀', poi_count: 10 },
        { district: '涵江区', score: 70, accessibility: '良好', poi_count: 6 },
        { district: '秀屿区', score: 50, accessibility: '一般', poi_count: 5 },
        { district: '仙游县', score: 45, accessibility: '一般', poi_count: 7 }
      ]
    }
  }
}

// 初始化价格图表
const initPriceChart = () => {
  if (!priceChartRef.value) return
  if (priceChart) priceChart.dispose()
  
  priceChart = echarts.init(priceChartRef.value)
  const data = housingStats.value
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.district),
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      name: '元/㎡',
      axisLine: { lineStyle: { color: '#3a3a5a' } },
      axisLabel: { color: '#a0a0b0' },
      splitLine: { lineStyle: { color: '#2a2a4a' } }
    },
    series: [{
      name: '均价',
      type: 'bar',
      data: data.map(d => d.avgPrice),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#FF6B6B' },
          { offset: 1, color: '#C41E3A' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }
  priceChart.setOption(option)
}

// 获取AI分析
const getAIAnalysis = async () => {
  aiLoading.value = true
  try {
    const response = await api.interpretAnalysis('accessibility', {
      service_type: selectedServiceType.value,
      ...accessibilityData.value
    })
    aiAnalysis.value = response.interpretation
  } catch (error) {
    const serviceName = selectedServiceType.value === 'hospital' ? '医疗' : '教育'
    aiAnalysis.value = `**${serviceName}服务可达性分析报告**

根据空间分析结果，莆田市${serviceName}资源分布呈现以下特点：

**1. 区域差异明显**
- 城厢区、荔城区作为主城区，${serviceName}设施密度较高，可达性较好
- 秀屿区、仙游县相对偏远，存在服务盲区

**2. 改善建议**
- 加强农村地区${serviceName}设施布局
- 优化${serviceName === '医疗' ? '急救网络' : '校车路线'}覆盖
- 推进${serviceName}资源均等化配置

**3. 重点关注**
- ${selectedServiceType.value === 'hospital' ? '秀屿区每千人床位数偏低' : '仙游县生师比偏高'}
- 建议增加${serviceName === '医疗' ? '基层医疗卫生站点' : '农村学校教师配置'}`
  } finally {
    aiLoading.value = false
  }
}

// 加载数据
onMounted(async () => {
  try {
    // 加载行政区划
    const districts = await api.getDistricts()
    districtsData.value = districts

    // 加载资源统计
    const resources = await api.getResourceStats()
    resourceData.value = resources

    // 初始分析
    await analyzeService()
  } catch (error) {
    console.error('数据加载失败:', error)
    // 使用模拟数据
    resourceData.value = {
      districts: [
        { name: '城厢区', hospitals: 8, hospital_beds: 2850, beds_per_1000: 6.09, schools: 45, teachers: 2800, students: 48000 },
        { name: '涵江区', hospitals: 6, hospital_beds: 1920, beds_per_1000: 4.44, schools: 38, teachers: 2200, students: 38500 },
        { name: '荔城区', hospitals: 10, hospital_beds: 3560, beds_per_1000: 6.27, schools: 52, teachers: 3400, students: 62000 },
        { name: '秀屿区', hospitals: 5, hospital_beds: 1680, beds_per_1000: 2.97, schools: 42, teachers: 2100, students: 45000 },
        { name: '仙游县', hospitals: 7, hospital_beds: 2450, beds_per_1000: 2.37, schools: 86, teachers: 4800, students: 98000 }
      ]
    }
    await analyzeService()
  }
})
</script>

<style scoped>
.service-view {
  height: 100%;
  display: flex;
}

.map-section {
  flex: 1;
  position: relative;
}

.analysis-panel {
  width: 400px;
  background: var(--bg-darker);
  border-left: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.service-selector {
  display: flex;
  justify-content: center;
}

.service-selector :deep(.el-radio-button__inner) {
  background: var(--bg-card);
  border-color: var(--border-color);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.service-selector :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: var(--mazu-red);
  border-color: var(--mazu-red);
  color: white;
}

.resource-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: center;
}

.stat-card .stat-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: var(--golden);
}

.stat-card .stat-label {
  font-size: 11px;
  color: var(--text-muted);
}

.accessibility-section h4,
.resource-table-section h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

/* 评分圆环 */
.overall-score {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--bg-card);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid;
}

.score-circle.excellent { border-color: #00C853; }
.score-circle.good { border-color: #FFD700; }
.score-circle.fair { border-color: #FF9800; }
.score-circle.poor { border-color: #F44336; }

.score-circle .score {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.score-circle .label {
  font-size: 10px;
  color: var(--text-muted);
}

.score-desc .assessment {
  font-size: 16px;
  font-weight: 600;
  color: var(--golden);
}

.score-desc p {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
}

/* 区县评分条 */
.district-scores {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.district-score-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.district-score-item .name {
  width: 60px;
  font-size: 12px;
  color: var(--text-secondary);
}

.score-bar-wrapper {
  flex: 1;
  height: 8px;
  background: var(--bg-card);
  border-radius: 4px;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.score-bar.excellent { background: linear-gradient(90deg, #00C853, #69F0AE); }
.score-bar.good { background: linear-gradient(90deg, #FFD700, #FFEB3B); }
.score-bar.fair { background: linear-gradient(90deg, #FF9800, #FFB74D); }
.score-bar.poor { background: linear-gradient(90deg, #F44336, #E57373); }

.district-score-item .score-text {
  width: 40px;
  font-size: 11px;
  color: var(--text-muted);
  text-align: right;
}

/* 表格样式 */
.resource-table-section :deep(.el-table) {
  background: transparent;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: var(--bg-card);
  --el-table-header-bg-color: var(--bg-darker);
  --el-table-text-color: var(--text-secondary);
  --el-table-header-text-color: var(--text-primary);
  --el-table-border-color: var(--border-color);
}

.resource-table-section :deep(.el-table th) {
  font-size: 12px;
}

.resource-table-section :deep(.el-table td) {
  font-size: 12px;
}

/* AI区域 */
.ai-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.ai-btn {
  background: linear-gradient(135deg, var(--mazu-red) 0%, var(--mazu-red-dark) 100%);
  border: none;
}

.ai-result {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
}

.ai-content {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.ai-content :deep(strong) {
  color: var(--golden);
}

.ai-content :deep(ul),
.ai-content :deep(ol) {
  padding-left: 16px;
  margin: 8px 0;
}

/* 住房分析 */
.housing-analysis h4 {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.price-chart {
  height: 200px;
  margin-bottom: 16px;
}

.price-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--bg-card);
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.price-stat-item .district {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
}

.price-stat-item .price {
  font-size: 14px;
  font-weight: 600;
  color: #FF6B6B;
}

.price-stat-item .count {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
