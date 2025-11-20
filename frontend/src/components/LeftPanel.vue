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
      <h1 class="panel-title">0dayAgent-ByGodice</h1>
      <div class="title-accent"></div>
    </div>

    <div class="panel-content">
      <div class="list-top">
        <div class="list-label">漏洞列表</div>
        <button class="list-manage" @click="toggleAllTargets">
          {{ allExpanded ? '全部收起' : '全部展开' }}
        </button>
      </div>
      <div class="target-list">
        <div v-for="target in vulnerableTargets" :key="target.ip" class="target-card">
          <button class="target-header" @click="toggleTarget(target.ip)">
            <div class="target-meta">
              <div class="target-ip">{{ target.ip }}</div>
              <div class="target-info">{{ target.site }}</div>
            </div>
            <div class="target-stats">
              <span class="target-count">{{ target.vulnerabilities.length }} 个漏洞</span>
              <span class="target-time">{{ target.lastSeen }}</span>
            </div>
            <span class="target-arrow" :class="{ open: isExpanded(target.ip) }"></span>
          </button>
          <transition name="collapse">
            <div v-if="isExpanded(target.ip)" class="vuln-list">
              <div
                v-for="vuln in target.vulnerabilities"
                :key="vuln.id"
                class="vuln-item"
              >
                <div class="vuln-main">
                  <div class="vuln-title">{{ vuln.title }}</div>
                  <div class="vuln-id">{{ vuln.id }}</div>
                </div>
                <div class="vuln-meta">
                  <span class="severity-tag" :class="getSeverityClass(vuln.severity)">
                    {{ getSeverityLabel(vuln.severity) }}
                  </span>
                  <span class="vuln-time">{{ vuln.time }}</span>
                </div>
              </div>
            </div>
          </transition>
        </div>
        <div v-if="vulnerableTargets.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="empty-text">暂无漏洞数据</p>
        </div>
      </div>
    </div>

    <div class="panel-buttons">
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
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const activeButton = ref(null)

const quickButtons = [
  { id: 'rag-config', text: 'RAG配置', icon: '📚' },
  { id: 'web-search', text: '网页搜索', icon: '🌐' }
]

const vulnerableTargets = ref([
  {
    ip: '192.168.1.10',
    site: '目标站点 A',
    lastSeen: '2024-01-15 14:30',
    vulnerabilities: [
      { id: 'VULN-001', title: 'SQL注入 - 登录接口', severity: 'high', time: '2024-01-15 14:20' },
      { id: 'VULN-002', title: '目录遍历 - 文件下载', severity: 'medium', time: '2024-01-15 13:05' }
    ]
  },
  {
    ip: '203.0.113.22',
    site: '目标站点 B',
    lastSeen: '2024-01-14 16:45',
    vulnerabilities: [
      { id: 'VULN-005', title: '任意文件上传', severity: 'high', time: '2024-01-14 16:30' },
      { id: 'VULN-006', title: '信息泄露 - 备份文件', severity: 'low', time: '2024-01-14 15:10' }
    ]
  },
  {
    ip: '10.0.0.5',
    site: '目标站点 C',
    lastSeen: '2024-01-13 11:20',
    vulnerabilities: [
      { id: 'VULN-010', title: '弱口令 - SSH', severity: 'medium', time: '2024-01-13 10:50' }
    ]
  }
])

const expandedTargets = ref({})

const ensureExpandedState = () => {
  vulnerableTargets.value.forEach((target) => {
    if (expandedTargets.value[target.ip] === undefined) {
      expandedTargets.value[target.ip] = true
    }
  })
}

ensureExpandedState()

const allExpanded = computed(() => vulnerableTargets.value.every((target) => expandedTargets.value[target.ip]))

const toggleTarget = (ip) => {
  expandedTargets.value[ip] = !expandedTargets.value[ip]
}

const isExpanded = (ip) => expandedTargets.value[ip]

const toggleAllTargets = () => {
  const nextState = !allExpanded.value
  vulnerableTargets.value.forEach((target) => {
    expandedTargets.value[target.ip] = nextState
  })
}

const severityMap = {
  high: '高危',
  medium: '中危',
  low: '低危'
}

const getSeverityLabel = (level) => severityMap[level] || level

const getSeverityClass = (level) => {
  switch (level) {
    case 'high':
      return 'severity-high'
    case 'medium':
      return 'severity-medium'
    case 'low':
      return 'severity-low'
    default:
      return ''
  }
}

const handleButtonClick = (id) => {
  activeButton.value = activeButton.value === id ? null : id
  console.log('点击了按钮:', id)
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

.list-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.list-label {
  font-size: 0.85rem;
  color: rgba(240, 247, 255, 0.85);
  letter-spacing: 0.02em;
}

.list-manage {
  background: transparent;
  border: 1px solid rgba(76, 206, 255, 0.25);
  color: #7dd3fc;
  border-radius: 999px;
  padding: 0.15rem 0.75rem;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.list-manage:hover {
  border-color: rgba(76, 206, 255, 0.5);
  color: #c3f0ff;
}

.target-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.target-card {
  background: rgba(33, 46, 88, 0.65);
  border: 1px solid rgba(132, 206, 255, 0.16);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.target-header {
  width: 100%;
  padding: 0.85rem;
  background: transparent;
  color: inherit;
  border: none;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.75rem;
  align-items: center;
  cursor: pointer;
  text-align: left;
}

.target-meta {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
}

.target-ip {
  font-size: 0.88rem;
  font-weight: 600;
  color: #f7fbff;
}

.target-info {
  font-size: 0.72rem;
  color: rgba(210, 220, 255, 0.75);
}

.target-stats {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  font-size: 0.7rem;
  color: rgba(199, 210, 254, 0.8);
}

.target-count {
  font-weight: 500;
  color: #8be5ff;
}

.target-arrow {
  width: 18px;
  height: 18px;
  border: 1px solid rgba(132, 206, 255, 0.4);
  border-radius: 50%;
  position: relative;
  transition: transform 0.2s ease;
}

.target-arrow::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 6px;
  height: 6px;
  border: solid rgba(255, 255, 255, 0.8);
  border-width: 0 0 1px 1px;
  transform: translate(-50%, -40%) rotate(-45deg);
}

.target-arrow.open {
  transform: rotate(180deg);
}

.vuln-list {
  padding: 0 0.85rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.vuln-item {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.65rem 0.5rem;
  background: rgba(16, 25, 56, 0.85);
  border: 1px solid rgba(132, 206, 255, 0.18);
  border-radius: 10px;
}

.vuln-main {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.vuln-title {
  font-size: 0.78rem;
  color: #f5f8ff;
}

.vuln-id {
  font-size: 0.68rem;
  color: rgba(199, 210, 254, 0.65);
}

.vuln-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
  font-size: 0.68rem;
  color: rgba(199, 210, 254, 0.8);
}

.severity-tag {
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-high {
  background: rgba(248, 113, 113, 0.18);
  color: #fecaca;
}

.severity-medium {
  background: rgba(251, 191, 36, 0.18);
  color: #fde68a;
}

.severity-low {
  background: rgba(52, 211, 153, 0.18);
  color: #bbf7d0;
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
}

.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.2s ease;
}

.collapse-enter-to,
.collapse-leave-from {
  max-height: 500px;
  opacity: 1;
}

.empty-state {
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(14, 18, 42, 0.45);
  border-top: 1px solid rgba(132, 206, 255, 0.2);
  justify-items: stretch;
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

</style>
