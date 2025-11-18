<template>
  <div class="app-container">
    <!-- 网格背景 -->
    <div class="grid-background"></div>
    
    <!-- 顶部日期栏 -->
    <div class="top-bar">
      <div class="date-section">
        <span class="date-label">Date:</span>
        <span class="date-value">{{ currentDate }}</span>
        <button class="config-button" type="button" @click="toggleConfigModal(true)">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M19.14 12.94c.04-.31.06-.63.06-.94s-.02-.63-.06-.94l2.03-1.58c.18-.14.23-.41.12-.62l-1.92-3.32a.5.5 0 0 0-.6-.22l-2.39.96a7.03 7.03 0 0 0-1.63-.94l-.36-2.54A.5.5 0 0 0 14.4 2h-3.8a.5.5 0 0 0-.5.42l-.36 2.54c-.59.24-1.14.55-1.63.94l-2.39-.96a.5.5 0 0 0-.6.22L2.3 8.02a.5.5 0 0 0 .12.62l2.03 1.58c-.04.31-.06.63-.06.94s.02.63.06.94l-2.03 1.58a.5.5 0 0 0-.12.62l1.92 3.32c.13.22.38.3.6.22l2.39-.96c.49.39 1.04.7 1.63.94l.36 2.54c.04.24.25.42.5.42h3.8c.25 0 .46-.18.5-.42l.36-2.54c.59-.24 1.14-.55 1.63-.94l2.39.96c.22.08.47 0 .6-.22l1.92-3.32a.5.5 0 0 0-.12-.62l-2.03-1.58ZM12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"
            />
          </svg>
          <span class="config-label">配置</span>
        </button>
      </div>
    </div>

    <div v-if="showConfigModal" class="modal-overlay" @click.self="toggleConfigModal(false)">
      <div class="modal-card">
        <div class="modal-header">
          <h2>系统配置</h2>
          <button class="close-button" type="button" @click="toggleConfigModal(false)">×</button>
        </div>
        <form class="modal-body" @submit.prevent="handleConfigSubmit">
          <label>
            <span>Base URL</span>
            <input v-model="baseUrl" type="text" placeholder="https://api.example.com" />
          </label>
          <label>
            <span>Model Name</span>
            <input v-model="modelName" type="text" placeholder="gpt-4.1" />
          </label>
          <label>
            <span>API Key</span>
            <input v-model="apiKey" type="password" placeholder="sk-..." />
          </label>
          <div class="modal-actions">
            <button class="ghost" type="button" @click="toggleConfigModal(false)">取消</button>
            <button class="primary" type="submit">保存</button>
          </div>
        </form>
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
const showConfigModal = ref(false)
const baseUrl = ref('')
const modelName = ref('')
const apiKey = ref('')

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

const toggleConfigModal = (visible) => {
  showConfigModal.value = visible
}

const handleConfigSubmit = async () => {
  const payload = {
    base_url: baseUrl.value,
    model_name: modelName.value,
    api_key: apiKey.value
  }

  try {
    const response = await fetch('http://localhost:8000/api/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`)
    }

    console.log('配置已保存', payload)
    toggleConfigModal(false)
  } catch (error) {
    console.error('保存配置失败', error)
    alert('保存配置失败，请检查后端服务是否已启动')
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

.config-button {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  border: 1px solid rgba(124, 210, 255, 0.35);
  background: rgba(20, 39, 86, 0.65);
  color: #c6e9ff;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.config-button svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.config-button:hover {
  transform: translateY(-1px);
  border-color: rgba(124, 210, 255, 0.6);
  background: rgba(29, 56, 116, 0.8);
}

.config-label {
  font-weight: 600;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(6, 10, 24, 0.6);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  padding: 1.5rem;
}

.modal-card {
  width: min(420px, 100%);
  background: rgba(17, 27, 58, 0.95);
  border: 1px solid rgba(124, 210, 255, 0.25);
  border-radius: 18px;
  box-shadow: 0 20px 60px rgba(5, 8, 22, 0.7);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #f7fbff;
}

.modal-header h2 {
  font-size: 1.1rem;
  letter-spacing: 0.05em;
}

.close-button {
  background: transparent;
  border: none;
  color: #9beaff;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #d9e9ff;
}

.modal-body label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.85rem;
  letter-spacing: 0.03em;
}

.modal-body input {
  background: rgba(11, 20, 48, 0.85);
  border: 1px solid rgba(124, 210, 255, 0.2);
  border-radius: 10px;
  padding: 0.65rem 0.75rem;
  color: #f7fbff;
  font-size: 0.85rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.modal-body input:focus {
  outline: none;
  border-color: rgba(124, 210, 255, 0.7);
  box-shadow: 0 0 0 2px rgba(124, 210, 255, 0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.modal-actions button {
  padding: 0.55rem 1.2rem;
  border-radius: 999px;
  border: 1px solid transparent;
  cursor: pointer;
  letter-spacing: 0.05em;
  font-size: 0.8rem;
}

.modal-actions .ghost {
  background: transparent;
  border-color: rgba(124, 210, 255, 0.3);
  color: #9beaff;
}

.modal-actions .primary {
  background: linear-gradient(120deg, #5bd0ff, #7ae1ff);
  color: #0b1836;
  font-weight: 600;
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
