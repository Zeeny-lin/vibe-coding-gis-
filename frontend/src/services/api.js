/**
 * API服务模块
 * 封装所有后端API调用
 */
import axios from 'axios'

// 创建axios实例
const http = axios.create({
    baseURL: '/api/v1',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 响应拦截器
http.interceptors.response.use(
    response => response.data,
    error => {
        console.error('API Error:', error)
        return Promise.reject(error)
    }
)

// API方法
const api = {
    // ========== 生态环境 ==========
    /**
     * 获取所有环境数据
     */
    getEnvironment() {
        return http.get('/environment')
    },

    /**
     * 获取空气质量数据
     */
    getAirQuality() {
        return http.get('/environment/air')
    },

    /**
     * 获取天气数据
     */
    getWeather() {
        return http.get('/environment/weather')
    },

    /**
     * 获取水环境数据
     */
    getWaterQuality() {
        return http.get('/environment/water')
    },

    // ========== 交通概况 ==========
    /**
     * 获取所有交通数据
     */
    getTransport() {
        return http.get('/transport')
    },

    /**
     * 获取铁路数据
     */
    getRailway() {
        return http.get('/transport/railway')
    },

    /**
     * 获取公路数据
     */
    getHighway() {
        return http.get('/transport/highway')
    },

    /**
     * 获取港口数据
     */
    getPorts() {
        return http.get('/transport/port')
    },

    /**
     * 获取交通设施GeoJSON
     */
    getTransportGeojson() {
        return http.get('/transport/geojson')
    },

    /**
     * 获取火车班次时刻表
     */
    getTrainSchedules() {
        return http.get('/transport/schedules/train')
    },

    /**
     * 获取轮渡班次时刻表
     */
    getFerrySchedules() {
        return http.get('/transport/schedules/ferry')
    },

    /**
     * 获取长途汽车班次
     */
    getBusSchedules() {
        return http.get('/transport/schedules/bus')
    },

    // ========== 行政区划 ==========
    /**
     * 获取所有行政区划数据
     */
    getDistricts() {
        return http.get('/districts')
    },

    /**
     * 获取单个区县数据
     * @param {string} name 区县名称
     */
    getDistrictByName(name) {
        return http.get(`/districts/${name}`)
    },

    /**
     * 获取区县名称列表
     */
    getDistrictNames() {
        return http.get('/districts/list/names')
    },

    // ========== POI兴趣点 ==========
    /**
     * 获取POI数据
     * @param {string} type POI类型
     * @param {string} district 区县名称
     */
    getPOI(type = null, district = null) {
        const params = {}
        if (type) params.type = type
        if (district) params.district = district
        return http.get('/poi', { params })
    },

    /**
     * 获取POI类型列表
     */
    getPOITypes() {
        return http.get('/poi/types')
    },

    /**
     * 获取POI统计
     */
    getPOIStats() {
        return http.get('/poi/stats')
    },

    /**
     * 获取景区范围多边形
     */
    getScenicAreas() {
        return http.get('/poi/scenic-areas')
    },

    // ========== 统计数据 ==========
    /**
     * 获取所有统计数据
     */
    getStatistics() {
        return http.get('/statistics')
    },

    /**
     * 获取人口统计数据
     */
    getPopulationStats() {
        return http.get('/statistics/population')
    },

    /**
     * 获取经济统计数据
     */
    getEconomyStats() {
        return http.get('/statistics/economy')
    },

    /**
     * 获取资源统计数据
     */
    getResourceStats() {
        return http.get('/statistics/resources')
    },

    /**
     * 获取特定区县统计
     * @param {string} name 区县名称
     */
    getDistrictStats(name) {
        return http.get(`/statistics/${name}`)
    },

    // ========== 空间分析 ==========
    /**
     * 路线规划
     * @param {Array} start 起点坐标 [lng, lat]
     * @param {Array} end 终点坐标 [lng, lat]
     * @param {Array} waypoints 途经点
     * @param {string} mode 出行方式: driving, walking, cycling, transit
     */
    planRoute(start, end, waypoints = null, mode = 'driving') {
        return http.post('/analysis/route', { start, end, waypoints, mode })
    },

    /**
     * 智能选址
     * @param {string} facilityType 设施类型
     * @param {Object} weights 权重配置
     */
    siteSelection(facilityType, weights = null) {
        return http.post('/analysis/site-selection', {
            facility_type: facilityType,
            weights
        })
    },

    /**
     * 可达性分析
     * @param {string} poiType POI类型
     * @param {number} threshold 距离阈值
     */
    accessibilityAnalysis(poiType, threshold = 3000) {
        return http.post('/analysis/accessibility', {
            poi_type: poiType,
            distance_threshold: threshold
        })
    },

    /**
     * 公共服务覆盖分析
     * @param {string} poiType POI类型
     * @param {number} bufferDistance 缓冲距离
     */
    serviceCoverage(poiType, bufferDistance = 2000) {
        return http.get('/analysis/service-coverage', {
            params: { poi_type: poiType, buffer_distance: bufferDistance }
        })
    },

    /**
     * 密度分析
     * @param {string} poiType POI类型
     * @param {number} cellSize 网格大小
     */
    densityAnalysis(poiType, cellSize = 1000) {
        return http.get('/analysis/density', {
            params: { poi_type: poiType, cell_size: cellSize }
        })
    },

    /**
     * 旅游路线推荐
     * @param {string} theme 主题
     * @param {number} duration 天数
     */
    tourismRoute(theme = 'mazu', duration = 1) {
        return http.get('/analysis/tourism-route', {
            params: { theme, duration }
        })
    },

    // ========== AI助手 ==========
    /**
   * AI聊天
   * @param {string} message 消息
   * @param {Array} history 历史消息
   * @param {Object} context 上下文
   * @param {string} model 模型名称
   */
    chat(message, history = null, context = null, model = null) {
        return http.post('/ai/chat', { message, model, history, context })
    },

    /**
     * AI分析解读
     * @param {string} analysisType 分析类型
     * @param {Object} data 分析数据
     */
    interpretAnalysis(analysisType, data) {
        return http.post('/ai/interpret', {
            analysis_type: analysisType,
            data
        })
    },

    /**
     * 获取AI建议
     * @param {string} topic 主题
     */
    getAISuggestions(topic = 'general') {
        return http.get('/ai/suggestions', { params: { topic } })
    },

    /**
     * 检查AI服务状态
     */
    checkAIStatus() {
        return http.get('/ai/status')
    },

    /**
     * 获取可用模型列表
     */
    getAvailableModels() {
        return http.get('/ai/models')
    },

    // ========== AI旅游助手 ==========
    /**
     * AI景点推荐
     * @param {Object} preferences 用户偏好 { duration: 天数, style: 风格 }
     */
    recommendTourismSpots(preferences = null) {
        return http.post('/ai/tourism/recommend-spots', { preferences })
    },

    /**
     * AI路线规划
     * @param {Array} spots 景点名称列表
     * @param {Object} preferences 偏好 { mode: 'driving'/'walking' }
     */
    planTourismRoute(spots, preferences = null) {
        return http.post('/ai/tourism/plan-route', { spots, preferences })
    },

    // ========== 统计年鉴 ==========
    /**
     * 获取年鉴汇总数据
     */
    getYearbook() {
        return http.get('/yearbook')
    },

    /**
     * 获取GDP历史数据
     */
    getYearbookGDP() {
        return http.get('/yearbook/gdp')
    },

    /**
     * 获取人口历史数据
     */
    getYearbookPopulation() {
        return http.get('/yearbook/population')
    },

    /**
     * 获取居民收入数据
     */
    getYearbookIncome() {
        return http.get('/yearbook/income')
    },

    // ========== 经济产业 ==========
    /**
     * 获取经济产业统计数据
     */
    getEconomyStats() {
        return http.get('/economy/stats')
    }
}

export default api
