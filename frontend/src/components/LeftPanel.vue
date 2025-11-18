<template>
  <div class="left-panel">
    <div class="panel-header">
      <div class="header-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <h1 class="panel-title">One-Click-Src</h1>
      <div class="title-accent"></div>
    </div>

    <div class="panel-content">
      <div class="history-top">
        <div class="history-label">历史对话</div>
        <button class="history-manage" @click="clearHistory">清空</button>
      </div>
      <div class="history-list">
        <div
          v-for="(item, index) in historyItems"
          :key="index"
          class="history-item"
          :class="{ active: selectedHistory === index }"
          @click="selectHistory(index)"
        >
          <div class="history-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="history-content">
            <div class="history-title">{{ item.title }}</div>
            <div class="history-time">{{ item.time }}</div>
          </div>
        </div>
        <div v-if="historyItems.length === 0" class="history-empty">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="empty-text">暂无历史对话</p>
        </div>
      </div>
    </div>

    <div class="panel-buttons">
      <div class="toggle-card" v-for="toggle in toggleCards" :key="toggle.id">
        <div class="toggle-header">
          <div class="toggle-icon">
            <span>{{ toggle.icon }}</span>
          </div>
          <div class="toggle-title">{{ toggle.title }}</div>
        </div>
        <button
          class="toggle-switch"
          :class="{ active: toggleStates[toggle.id] }"
          @click="handleToggle(toggle.id)"
        >
          <span class="switch-thumb"></span>
        </button>
      </div>

      <button
        v-for="button in quickButtons"
        :key="button.id"
        class="action-button"
        :class="{ active: activeButton === button.id }"
        @click="handleButtonClick(button.id)"
      >
        <div class="button-icon-wrapper">
          <span class="button-icon">{{ button.icon }}</span>
        </div>
        <span class="button-text">{{ button.text }}</span>
        <div class="button-glow"></div>
      </button>
    </div>

    <!-- 自动渗透模态 -->
    <Teleport to="body">
      <div v-if="showVulnModal" class="modal-mask">
        <div class="modal-panel">
          <div class="modal-header">
            <div>
              <h3>选择漏洞类型</h3>
              <p>关闭自动渗透时可按需选择需要处理的漏洞类别</p>
            </div>
            <button class="modal-close" @click="closeVulnModal(false)">×</button>
          </div>
          <div class="modal-options">
            <label
              v-for="option in vulnerabilityOptions"
              :key="option.value"
              class="modal-option"
            >
              <input type="checkbox" :value="option.value" v-model="selectedVulnerabilities" />
              <span>{{ option.label }}</span>
            </label>
          </div>
          <div class="modal-actions">
            <button class="ghost-btn" @click="closeVulnModal(false)">取消</button>
            <button class="primary-btn" @click="closeVulnModal(true)">确认策略</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 自动工具模态 -->
    <Teleport to="body">
      <div v-if="showToolModal" class="modal-mask">
        <div class="modal-panel">
          <div class="modal-header">
            <div>
              <h3>选择需要调用的工具</h3>
              <p>关闭全自动Tool Call后可手动选择模型可调用的工具</p>
            </div>
            <button class="modal-close" @click="closeToolModal(false)">×</button>
          </div>
          <div class="modal-options">
            <label
              v-for="tool in toolOptions"
              :key="tool.value"
              class="modal-option"
            >
              <input type="checkbox" :value="tool.value" v-model="selectedTools" />
              <span>{{ tool.label }}</span>
            </label>
          </div>
          <div class="modal-actions">
            <button class="ghost-btn" @click="closeToolModal(false)">取消</button>
            <button class="primary-btn" @click="closeToolModal(true)">应用工具</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeButton = ref(null)
const selectedHistory = ref(null)

const historyItems = ref([
  { title: '渗透测试会话 #1', time: '2024-01-15 14:30' },
  { title: '漏洞扫描任务', time: '2024-01-15 10:20' },
  { title: '系统安全评估', time: '2024-01-14 16:45' }
])

const quickButtons = [
  { id: 'rag-config', text: 'RAG配置', icon: '📚' },
  { id: 'web-search', text: '网页搜索', icon: '🌐' }
]

const toggleStates = reactive({
  'auto-penetrate': true,
  'auto-tool': true
})

const toggleCards = [
  {
    id: 'auto-penetrate',
    title: '自动渗透',
    icon: '🎯'
  },
  {
    id: 'auto-tool',
    title: '自动工具',
    icon: '🛠️'
  }
]

const vulnerabilityOptions = [
  { value: 'file-upload', label: '任意文件上传' },
  { value: 'path-traversal', label: '目录遍历' },
  { value: 'xss', label: 'XSS' },
  { value: 'sql-injection', label: 'SQL注入' },
  { value: 'command-injection', label: '命令注入' }
]

const toolOptions = [
  { value: 'dirsearch', label: 'dirsearch' },
  { value: 'sqlmap', label: 'sqlmap' },
  { value: 'nmap', label: 'nmap' }
]

const selectedVulnerabilities = ref(vulnerabilityOptions.map((option) => option.value))
const selectedTools = ref(toolOptions.map((tool) => tool.value))
const showVulnModal = ref(false)
const showToolModal = ref(false)

const handleButtonClick = (id) => {
  activeButton.value = activeButton.value === id ? null : id
  console.log('点击了按钮:', id)
}

const selectHistory = (index) => {
  selectedHistory.value = selectedHistory.value === index ? null : index
  console.log('选择了历史记录:', index)
}

const clearHistory = () => {
  historyItems.value = []
  selectedHistory.value = null
}

const handleToggle = (id) => {
  const nextState = !toggleStates[id]
  toggleStates[id] = nextState

  if (!nextState) {
    if (id === 'auto-penetrate') {
      showVulnModal.value = true
    } else if (id === 'auto-tool') {
      showToolModal.value = true
    }
  } else {
    if (id === 'auto-penetrate') {
      showVulnModal.value = false
    } else if (id === 'auto-tool') {
      showToolModal.value = false
    }
  }
}

const closeVulnModal = (confirmed) => {
  if (!confirmed) {
    toggleStates['auto-penetrate'] = true
  }
  showVulnModal.value = false
  console.log('漏洞策略:', selectedVulnerabilities.value)
}

const closeToolModal = (confirmed) => {
  if (!confirmed) {
    toggleStates['auto-tool'] = true
  }
  showToolModal.value = false
  console.log('工具策略:', selectedTools.value)
}
</script>

<style scoped>
.left-panel {
  flex: 0 0 20%;
  display: flex;
  flex-direction: column;
  background: rgba(27, 39, 78, 0.9);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  box-shadow:
    0 10px 32px rgba(7, 11, 24, 0.58),
    0 0 0 1px rgba(132, 206, 255, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  overflow: hidden;
  border: 1px solid rgba(132, 206, 255, 0.22);
  position: relative;
  min-width: 0;
}

.left-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(76, 206, 255, 0.6), transparent);
  z-index: 1;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.25rem 1rem;
  border-bottom: 1px solid rgba(76, 206, 255, 0.15);
  position: relative;
  flex-wrap: wrap;
}

.header-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4cd4ff;
  opacity: 0.9;
  flex-shrink: 0;
}

.header-icon svg {
  width: 16px;
  height: 16px;
  filter: drop-shadow(0 0 4px rgba(76, 206, 255, 0.55));
}

.panel-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: #f0f7ff;
  position: relative;
  line-height: 1.2;
}

.title-accent {
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 42px;
  height: 2px;
  background: linear-gradient(90deg, #4cd4ff, transparent);
  box-shadow: 0 0 10px rgba(76, 206, 255, 0.6);
}

.panel-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.history-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.history-label {
  font-size: 0.85rem;
  color: rgba(240, 247, 255, 0.8);
}

.history-manage {
  background: transparent;
  border: 1px solid rgba(76, 206, 255, 0.25);
  color: #7dd3fc;
  border-radius: 999px;
  padding: 0.15rem 0.75rem;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-manage:hover {
  border-color: rgba(76, 206, 255, 0.5);
  color: #c3f0ff;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(33, 46, 88, 0.6);
  border: 1px solid rgba(132, 206, 255, 0.16);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.history-item:hover {
  background: rgba(33, 46, 88, 0.8);
  border-color: rgba(132, 206, 255, 0.35);
  transform: translateX(2px);
}

.history-item.active {
  background: rgba(140, 230, 255, 0.22);
  border-color: rgba(140, 230, 255, 0.45);
  box-shadow: 0 0 18px rgba(140, 230, 255, 0.28);
}

.history-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8be5ff;
  opacity: 0.8;
  flex-shrink: 0;
}

.history-icon svg {
  width: 18px;
  height: 18px;
}

.history-content {
  flex: 1;
  min-width: 0;
}

.history-title {
  font-size: 0.8rem;
  font-weight: 500;
  color: #f9fcff;
  margin-bottom: 0.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 0.68rem;
  color: rgba(210, 220, 255, 0.75);
}

.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: rgba(199, 210, 254, 0.7);
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4cd4ff;
  opacity: 0.35;
}

.empty-text {
  font-size: 0.75rem;
  margin: 0;
}

.panel-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(14, 18, 42, 0.45);
  border-top: 1px solid rgba(132, 206, 255, 0.2);
  justify-items: stretch;
}

.toggle-card {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  padding: 0.8rem 0.75rem;
  background: rgba(36, 49, 96, 0.65);
  border: 1px solid rgba(132, 206, 255, 0.24);
  border-radius: 12px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  min-height: 100px;
  align-items: center;
}

.toggle-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  justify-content: center;
}

.toggle-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(140, 230, 255, 0.16);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.toggle-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #f9fbff;
}

.toggle-switch {
  position: relative;
  width: 40px;
  height: 24px;
  border-radius: 999px;
  border: 1px solid rgba(132, 206, 255, 0.35);
  background: rgba(22, 30, 54, 0.75);
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  align-self: center;
}

.toggle-switch .switch-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(220, 228, 255, 0.85);
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
}

.toggle-switch.active {
  background: linear-gradient(135deg, #8ce6ff, #6ea5ff);
  border-color: transparent;
}

.toggle-switch.active .switch-thumb {
  left: 20px;
  background: #081225;
}

.action-button {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.85rem 0.5rem;
  background: rgba(36, 49, 96, 0.62);
  border: 1px solid rgba(132, 206, 255, 0.22);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  overflow: hidden;
  width: 100%;
  min-height: 100px;
}

.action-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 206, 255, 0.15), transparent);
  transition: left 0.5s;
}

.action-button:hover::before {
  left: 100%;
}

.action-button:hover {
  background: rgba(36, 49, 96, 0.82);
  transform: translateY(-2px);
  border-color: rgba(132, 206, 255, 0.4);
  box-shadow:
    0 4px 16px rgba(5, 8, 20, 0.45),
    0 0 20px rgba(76, 206, 255, 0.2);
}

.action-button.active {
  background: rgba(140, 230, 255, 0.25);
  border-color: rgba(140, 230, 255, 0.6);
  box-shadow:
    0 4px 20px rgba(76, 206, 255, 0.3),
    0 0 30px rgba(76, 206, 255, 0.25),
    inset 0 0 18px rgba(76, 206, 255, 0.12);
}

.button-icon-wrapper {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(132, 206, 255, 0.18);
  border-radius: 8px;
  border: 1px solid rgba(132, 206, 255, 0.25);
}

.button-icon {
  font-size: 1rem;
  line-height: 1;
  filter: drop-shadow(0 0 4px rgba(76, 206, 255, 0.35));
}

.button-text {
  font-size: 0.72rem;
  font-weight: 500;
  color: #f7fbff;
  letter-spacing: -0.01em;
  text-align: center;
}

.button-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(76, 206, 255, 0.35), transparent);
  transition: width 0.3s, height 0.3s;
  pointer-events: none;
}

.action-button.active .button-glow {
  width: 120px;
  height: 120px;
}

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(3, 8, 20, 0.75);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-panel {
  width: min(480px, 90vw);
  background: #0f1a33;
  border-radius: 18px;
  border: 1px solid rgba(76, 206, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
  padding: 1.5rem;
  color: #f0f7ff;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.modal-header p {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: rgba(226, 232, 255, 0.7);
}

.modal-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.25rem;
  cursor: pointer;
}

.modal-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.modal-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 0.75rem;
  background: rgba(26, 36, 70, 0.6);
  border: 1px solid rgba(76, 206, 255, 0.2);
  border-radius: 10px;
  font-size: 0.85rem;
}

.modal-option input {
  accent-color: #4cd4ff;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.ghost-btn,
.primary-btn {
  border-radius: 10px;
  padding: 0.55rem 1.2rem;
  font-size: 0.85rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.ghost-btn {
  background: rgba(255, 255, 255, 0.08);
  color: #c7d2fe;
}

.ghost-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.primary-btn {
  background: linear-gradient(135deg, #4cd4ff, #4b7dff);
  color: #081225;
  font-weight: 600;
  box-shadow: 0 6px 16px rgba(76, 206, 255, 0.35);
}

.primary-btn:hover {
  box-shadow: 0 8px 20px rgba(76, 206, 255, 0.45);
}
</style>
