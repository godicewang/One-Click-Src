<template>
  <div class="message-list">
    <div 
      v-for="message in messages" 
      :key="message.id"
      class="message-item"
      :class="message.type"
    >
      <div class="message-icon">
        <div v-if="message.type === 'ai'" class="ai-icon">
          <span class="ai-text">Ai</span>
          <div class="ai-pulse"></div>
        </div>
        <div v-else class="user-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
      <div class="message-content">
        <div class="message-text">{{ message.content }}</div>
        <div class="message-dash"></div>
      </div>
      <div class="message-action">
        <button class="stop-button" @click="handleStop(message.id)">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
            <line x1="8" y1="8" x2="16" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  messages: {
    type: Array,
    default: () => []
  }
})

const handleStop = (messageId) => {
  console.log('停止消息:', messageId)
}
</script>

<style scoped>
.message-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
  background: rgba(30, 42, 84, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 18px;
  box-shadow:
    0 12px 32px rgba(6, 10, 24, 0.58),
    0 0 0 1px rgba(132, 206, 255, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  overflow-y: auto;
  max-height: calc(100vh - 220px);
  border: 1px solid rgba(132, 206, 255, 0.22);
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: rgba(36, 48, 94, 0.62);
  border-radius: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(132, 206, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.message-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, #8ce6ff, transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.message-item:hover {
  background: rgba(36, 48, 94, 0.82);
  transform: translateX(4px);
  border-color: rgba(132, 206, 255, 0.4);
  box-shadow: 0 8px 18px rgba(6, 10, 24, 0.48);
}

.message-item:hover::before {
  opacity: 1;
}

.message-item.ai {
  background: rgba(140, 230, 255, 0.22);
  border-color: rgba(140, 230, 255, 0.45);
}

.message-item.ai:hover {
  background: rgba(140, 230, 255, 0.3);
  box-shadow:
    0 8px 20px rgba(6, 10, 24, 0.5),
    0 0 26px rgba(140, 230, 255, 0.28);
}

.message-icon {
  flex-shrink: 0;
}

.ai-icon {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8ce6ff, #79a8ff);
  color: #081326;
  border-radius: 50%;
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  box-shadow:
    0 0 20px rgba(140, 230, 255, 0.55),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.ai-pulse {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  border: 2px solid rgba(140, 230, 255, 0.9);
  animation: aiPulse 2s ease-in-out infinite;
  opacity: 0;
}

@keyframes aiPulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

.ai-text {
  position: relative;
  z-index: 1;
}

.user-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  color: #e8e8ed;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.user-icon svg {
  width: 18px;
  height: 18px;
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.message-text {
  color: #f9fcff;
  font-size: 0.9375rem;
  line-height: 1.47;
  letter-spacing: -0.01em;
  font-weight: 400;
}

.message-item.ai .message-text {
  color: #e8e8ed;
}

.message-dash {
  height: 0.5px;
  background: repeating-linear-gradient(
    to right,
    rgba(140, 230, 255, 0.45) 0px,
    rgba(140, 230, 255, 0.45) 3px,
    transparent 3px,
    transparent 6px
  );
  margin-top: 0.25rem;
}

.message-action {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-item:hover .message-action {
  opacity: 1;
}

.stop-button {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(255, 145, 123, 0.5);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #ff977f;
  padding: 0;
}

.stop-button:hover {
  background: rgba(255, 145, 123, 0.25);
  border-color: #ff977f;
  transform: scale(1.1);
  box-shadow: 0 0 12px rgba(255, 145, 123, 0.45);
}

.stop-button:active {
  transform: scale(0.95);
}

.stop-button svg {
  width: 14px;
  height: 14px;
}
</style>
