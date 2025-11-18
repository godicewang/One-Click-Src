<template>
  <div class="app-container">
    <!-- 网格背景 -->
    <div class="grid-background"></div>
    
    <!-- 顶部日期栏 -->
    <div class="top-bar">
      <div class="date-section">
        <span class="date-label">Date:</span>
        <span class="date-value">{{ currentDate }}</span>
        <div class="status-indicator">
          <span class="status-dot"></span>
          <span class="status-text">Online</span>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧主面板 -->
      <LeftPanel />

      <!-- 中间消息区域 -->
      <div class="center-panel">
        <MessageList :messages="messages" />
        <InputBox @send="handleSend" />
      </div>

      <!-- 右侧进度栏 -->
      <ProgressPanel :items="progressItems" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import LeftPanel from './components/LeftPanel.vue'
import MessageList from './components/MessageList.vue'
import InputBox from './components/InputBox.vue'
import ProgressPanel from './components/ProgressPanel.vue'

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const messages = ref([])

const progressItems = ref([
  { id: 1, title: '环境检测', description: '准备开始自动渗透测试...', status: '运行中' },
  { id: 2, title: '资产扫描', description: '正在扫描目标系统...', status: '等待' },
  { id: 3, title: '漏洞分析', description: '发现潜在漏洞，正在分析...', status: '未开始' }
])

const handleSend = (text) => {
  if (text.trim()) {
    messages.value.push({
      id: messages.value.length + 1,
      type: 'user',
      content: text
    })
    // 模拟AI回复
    setTimeout(() => {
      messages.value.push({
        id: messages.value.length + 1,
        type: 'ai',
        content: '收到您的指令，正在处理...'
      })
    }, 1000)
  }
}
</script>

<style scoped>
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: radial-gradient(circle at 25% 20%, rgba(110, 167, 255, 0.25), transparent 55%),
    linear-gradient(135deg, #131f37 0%, #253a66 55%, #131c33 100%);
  overflow: hidden;
  position: relative;
}

.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(124, 210, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124, 210, 255, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

.top-bar {
  position: relative;
  z-index: 1;
  padding: 1.25rem 2.5rem;
  background: rgba(24, 36, 74, 0.72);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(132, 206, 255, 0.2);
}

.date-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #f7fbff;
  font-weight: 400;
  font-size: 0.875rem;
  letter-spacing: 0.02em;
}

.date-label {
  opacity: 0.6;
  font-weight: 400;
}

.date-value {
  font-weight: 500;
  opacity: 0.9;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
  padding-left: 1rem;
  border-left: 1px solid rgba(124, 210, 255, 0.25);
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #8ce6ff;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(140, 230, 255, 0.9);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 8px rgba(0, 217, 255, 0.8);
  }
  50% {
    opacity: 0.6;
    box-shadow: 0 0 12px rgba(0, 217, 255, 1);
  }
}

.status-text {
  font-size: 0.75rem;
  color: #9beaff;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.main-content {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  gap: 1.25rem;
  padding: 1.25rem;
  overflow: hidden;
}

.center-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 0;
}
</style>
