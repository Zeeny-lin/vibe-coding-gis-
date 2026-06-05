<template>
  <div 
    class="ai-panel" 
    ref="panelRef"
    :style="{ top: panelPosition.y + 'px', right: panelPosition.x + 'px' }"
  >
    <!-- 头部（可拖动） -->
    <div 
      class="ai-panel-header" 
      @mousedown="startDrag"
      style="cursor: move;"
    >
      <span class="ai-panel-title">
        <el-icon><ChatDotRound /></el-icon>
        AI智能助手
      </span>
      <el-button 
        :icon="Close" 
        circle 
        size="small" 
        @click="$emit('close')"
        style="background: transparent; border: none; color: white;"
      />
    </div>

    <!-- 模型选择 -->
    <div class="model-selector">
      <el-select 
        v-model="selectedModel" 
        size="small" 
        placeholder="选择模型"
        @change="onModelChange"
      >
        <el-option 
          v-for="model in availableModels" 
          :key="model" 
          :label="getModelDisplayName(model)" 
          :value="model"
        />
      </el-select>
    </div>

    <!-- 消息区域 -->
    <div class="ai-panel-body" ref="messageContainer">
      <!-- 欢迎消息 -->
      <div class="chat-message assistant" v-if="messages.length === 0">
        <div class="message-content">
          👋 您好！我是莆田市情AI助手，可以为您介绍莆田的文化、旅游、经济等各方面情况。
          <div class="suggestions">
            <p>您可以问我：</p>
            <el-button 
              v-for="(suggestion, index) in suggestions" 
              :key="index"
              size="small" 
              @click="sendMessage(suggestion)"
              class="suggestion-btn"
            >
              {{ suggestion }}
            </el-button>
          </div>
        </div>
      </div>

      <!-- 聊天消息 -->
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        class="chat-message" 
        :class="msg.role"
      >
        <div class="message-content" v-html="formatMessage(msg.content)"></div>
      </div>

      <!-- 加载指示器 -->
      <div class="chat-message assistant" v-if="loading">
        <div class="message-content loading">
          <span class="typing-indicator">
            <span></span><span></span><span></span>
          </span>
          正在思考中...
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="ai-panel-footer">
      <div class="ai-input-wrapper">
        <el-input
          v-model="inputMessage"
          placeholder="请输入您的问题..."
          @keyup.enter="sendMessage()"
          :disabled="loading"
          class="ai-input"
        />
        <el-button 
          type="primary" 
          :icon="Promotion" 
          @click="sendMessage()"
          :loading="loading"
          class="send-btn"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, reactive } from 'vue'
import { ChatDotRound, Close, Promotion } from '@element-plus/icons-vue'
import { marked } from 'marked'
import api from '@/services/api'

const emit = defineEmits(['close'])

// 状态
const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messageContainer = ref(null)
const panelRef = ref(null)

// 模型相关
const availableModels = ref([])
const selectedModel = ref('')

// 面板位置（right和top的偏移）
const panelPosition = reactive({ x: 24, y: 96 })

// 推荐问题
const suggestions = [
  '介绍一下莆田市',
  '推荐妈祖文化旅游路线',
  '莆田有哪些美食？'
]

// 获取模型显示名称
const getModelDisplayName = (model) => {
  const nameMap = {
    'deepseek-ai/DeepSeek-V3': 'DeepSeek V3',
    'deepseek-ai/DeepSeek-R1': 'DeepSeek R1',
    'Qwen/Qwen2.5-72B-Instruct': 'Qwen 72B',
    'Qwen/Qwen2.5-32B-Instruct': 'Qwen 32B',
    'THUDM/glm-4-9b-chat': 'GLM-4 9B'
  }
  return nameMap[model] || model.split('/').pop()
}

// 模型切换
const onModelChange = () => {
  console.log('切换模型:', selectedModel.value)
}

// 加载可用模型
const loadModels = async () => {
  try {
    const result = await api.getAvailableModels()
    availableModels.value = result.models || []
    selectedModel.value = result.current || (availableModels.value[0] || '')
  } catch (error) {
    console.error('加载模型列表失败:', error)
    availableModels.value = ['deepseek-ai/DeepSeek-V3']
    selectedModel.value = 'deepseek-ai/DeepSeek-V3'
  }
}

// 发送消息
const sendMessage = async (text = null) => {
  const message = text || inputMessage.value.trim()
  if (!message || loading.value) return

  // 添加用户消息
  messages.value.push({ role: 'user', content: message })
  inputMessage.value = ''
  
  // 滚动到底部
  await scrollToBottom()

  // 调用AI接口
  loading.value = true
  try {
    const response = await api.chat(
      message, 
      messages.value.slice(0, -1), 
      null, 
      selectedModel.value
    )
    messages.value.push({ 
      role: 'assistant', 
      content: response.response || response 
    })
  } catch (error) {
    messages.value.push({ 
      role: 'assistant', 
      content: '抱歉，AI服务暂时不可用。请检查后端服务是否正常运行。\n\n您可以尝试：\n1. 确保后端服务已启动\n2. 检查网络连接\n3. 稍后重试' 
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

// 格式化消息（支持Markdown）
const formatMessage = (content) => {
  try {
    return marked.parse(content)
  } catch {
    return content
  }
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// 拖动相关
let isDragging = false
let dragStartX = 0
let dragStartY = 0
let startRight = 0
let startTop = 0

const startDrag = (e) => {
  isDragging = true
  dragStartX = e.clientX
  dragStartY = e.clientY
  startRight = panelPosition.x
  startTop = panelPosition.y
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
  if (!isDragging) return
  
  const deltaX = dragStartX - e.clientX
  const deltaY = e.clientY - dragStartY
  
  panelPosition.x = Math.max(0, startRight + deltaX)
  panelPosition.y = Math.max(60, startTop + deltaY)
}

const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 初始化
onMounted(() => {
  loadModels()
})
</script>

<style scoped>
.ai-panel {
  position: fixed;
  width: 400px;
  max-height: 600px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  z-index: 999;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ai-panel-header {
  padding: var(--spacing-md) var(--spacing-lg);
  background: linear-gradient(135deg, var(--mazu-red) 0%, var(--mazu-red-dark) 100%);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
}

.ai-panel-title {
  font-weight: 600;
  color: white;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* 模型选择器 */
.model-selector {
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-darker);
}

.model-selector :deep(.el-select) {
  width: 100%;
}

.model-selector :deep(.el-input__wrapper) {
  background: var(--bg-card);
  border-color: var(--border-color);
  box-shadow: none;
}

.model-selector :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 12px;
}

.ai-panel-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
  max-height: 380px;
}

.ai-panel-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.ai-input-wrapper {
  display: flex;
  gap: var(--spacing-sm);
}

.ai-input :deep(.el-input__wrapper) {
  background: var(--bg-darker);
  border: 1px solid var(--border-color);
  box-shadow: none;
}

.ai-input :deep(.el-input__inner) {
  color: var(--text-primary);
}

.send-btn {
  background: linear-gradient(135deg, var(--mazu-red) 0%, var(--mazu-red-dark) 100%);
  border: none;
}

/* 消息样式 */
.chat-message {
  margin-bottom: var(--spacing-md);
  display: flex;
  flex-direction: column;
}

.chat-message.user {
  align-items: flex-end;
}

.chat-message.assistant {
  align-items: flex-start;
}

.message-content {
  max-width: 90%;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 14px;
  line-height: 1.6;
}

.chat-message.user .message-content {
  background: var(--mazu-red);
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.assistant .message-content {
  background: var(--bg-darker);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

/* Markdown内容样式 */
.message-content :deep(p) {
  margin: 0 0 8px 0;
}

.message-content :deep(p:last-child) {
  margin-bottom: 0;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}

.message-content :deep(strong) {
  color: var(--golden);
}

/* 推荐问题 */
.suggestions {
  margin-top: 12px;
}

.suggestions p {
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-size: 12px;
}

.suggestion-btn {
  margin: 4px 4px 4px 0;
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 12px;
}

.suggestion-btn:hover {
  border-color: var(--mazu-red);
  color: var(--mazu-red);
}

/* 加载指示器 */
.typing-indicator {
  display: inline-flex;
  gap: 4px;
  margin-right: 8px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: var(--mazu-red);
  border-radius: 50%;
  animation: typing 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
