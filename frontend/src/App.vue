<template>
  <div id="app-root">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="header-logo">
        <span class="logo-icon">🌊</span>
        <h1 class="header-title">莆田市市情WebGIS系统</h1>
      </div>
      <div class="header-actions">
        <el-tooltip content="全屏" placement="bottom">
          <el-button :icon="FullScreen" circle @click="toggleFullscreen" />
        </el-tooltip>
        <el-tooltip content="帮助" placement="bottom">
          <el-button :icon="QuestionFilled" circle @click="showHelp = true" />
        </el-tooltip>
      </div>
    </header>

    <!-- 主体区域 -->
    <div class="app-container">
      <!-- 侧边导航 -->
      <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
        <nav class="nav-menu">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: $route.path === item.path }"
          >
            <el-icon class="icon">
              <component :is="item.icon" />
            </el-icon>
            <span class="label" v-show="!sidebarCollapsed">{{ item.label }}</span>
          </router-link>
        </nav>
        
        <!-- 侧边栏折叠按钮 -->
        <div class="sidebar-toggle" @click="sidebarCollapsed = !sidebarCollapsed">
          <el-icon>
            <ArrowLeft v-if="!sidebarCollapsed" />
            <ArrowRight v-else />
          </el-icon>
        </div>
      </aside>

      <!-- 内容区域 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- AI助手浮动按钮（可拖动） -->
    <button 
      class="ai-assistant-trigger" 
      ref="aiButtonRef"
      :style="{ right: aiButtonPos.x + 'px', bottom: aiButtonPos.y + 'px' }"
      @click="handleAIButtonClick"
      @mousedown="startAIButtonDrag"
    >
      <el-icon class="icon">
        <ChatDotRound />
      </el-icon>
    </button>

    <!-- AI助手面板 -->
    <AIAssistant v-if="aiPanelVisible" @close="aiPanelVisible = false" />

    <!-- 帮助弹窗 -->
    <el-dialog v-model="showHelp" title="系统帮助" width="600px">
      <div class="help-content">
        <h3>🌊 莆田市市情WebGIS系统</h3>
        <p>本系统融入妈祖文化特色，集成AI智能分析功能，为您展示莆田市的全方位市情数据。</p>
        
        <h4>功能模块</h4>
        <ul>
          <li><strong>首页概览</strong>：查看莆田市整体概况和关键指标</li>
          <li><strong>人口分布</strong>：可视化各区县人口分布情况</li>
          <li><strong>经济产业</strong>：分析各区县经济发展数据</li>
          <li><strong>文化旅游</strong>：探索妈祖文化旅游路线</li>
          <li><strong>公共服务</strong>：评估医疗教育资源分布</li>
        </ul>
        
        <h4>AI助手</h4>
        <p>点击右下角的AI助手按钮，可以进行自然语言问答，获取莆田市情介绍和分析建议。</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { 
  HomeFilled, 
  User, 
  TrendCharts, 
  Place, 
  OfficeBuilding,
  Sunny,
  Van,
  DataAnalysis,
  FullScreen,
  QuestionFilled,
  ChatDotRound,
  ArrowLeft,
  ArrowRight
} from '@element-plus/icons-vue'
import AIAssistant from '@/components/AIAssistant.vue'

// 导航菜单项
const navItems = [
  { path: '/', label: '首页概览', icon: HomeFilled },
  { path: '/population', label: '人口分布', icon: User },
  { path: '/economy', label: '经济产业', icon: TrendCharts },
  { path: '/tourism', label: '文化旅游', icon: Place },
  { path: '/environment', label: '生态环境', icon: Sunny },
  { path: '/transport', label: '交通概况', icon: Van },
  { path: '/service', label: '公共服务', icon: OfficeBuilding },
  { path: '/yearbook', label: '统计年鉴', icon: DataAnalysis }
]

// 状态
const sidebarCollapsed = ref(false)
const aiPanelVisible = ref(false)
const showHelp = ref(false)
const aiButtonRef = ref(null)

// AI按钮位置
const aiButtonPos = reactive({ x: 24, y: 24 })

// AI按钮拖动状态
let isDragging = false
let hasDragged = false
let startX = 0
let startY = 0
let startPosX = 0
let startPosY = 0

// 开始拖动AI按钮
const startAIButtonDrag = (e) => {
  isDragging = true
  hasDragged = false
  startX = e.clientX
  startY = e.clientY
  startPosX = aiButtonPos.x
  startPosY = aiButtonPos.y
  
  document.addEventListener('mousemove', onAIButtonDrag)
  document.addEventListener('mouseup', stopAIButtonDrag)
}

// 拖动中
const onAIButtonDrag = (e) => {
  if (!isDragging) return
  
  const deltaX = startX - e.clientX
  const deltaY = startY - e.clientY
  
  if (Math.abs(deltaX) > 5 || Math.abs(deltaY) > 5) {
    hasDragged = true
  }
  
  const newX = Math.max(10, Math.min(window.innerWidth - 70, startPosX + deltaX))
  const newY = Math.max(10, Math.min(window.innerHeight - 70, startPosY + deltaY))
  
  aiButtonPos.x = newX
  aiButtonPos.y = newY
}

// 停止拖动
const stopAIButtonDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onAIButtonDrag)
  document.removeEventListener('mouseup', stopAIButtonDrag)
}

// 处理AI按钮点击
const handleAIButtonClick = () => {
  if (!hasDragged) {
    aiPanelVisible.value = !aiPanelVisible.value
  }
}

// 全屏切换
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}
</script>

<style scoped>
/* 根容器 - 关键布局修复 */
#app-root {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏切换按钮 */
.sidebar-toggle {
  padding: var(--spacing-md);
  text-align: center;
  cursor: pointer;
  border-top: 1px solid var(--border-color);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.sidebar-toggle:hover {
  color: var(--mazu-red);
  background: var(--bg-card-hover);
}

/* 头部操作按钮 */
.header-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.header-actions .el-button {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.header-actions .el-button:hover {
  border-color: var(--mazu-red);
  color: var(--mazu-red);
}

/* Logo图标 */
.logo-icon {
  font-size: 28px;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 帮助内容 */
.help-content h3 {
  margin-bottom: 16px;
  color: var(--mazu-red);
}

.help-content h4 {
  margin: 16px 0 8px;
  color: var(--golden);
}

.help-content ul {
  padding-left: 20px;
}

.help-content li {
  margin-bottom: 8px;
}
</style>
