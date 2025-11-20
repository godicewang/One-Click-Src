<template>
  <div class="input-box">
    <div class="input-wrapper">
      <input
        v-model="inputText"
        type="text"
        placeholder="请输入目标网站 IP 地址"
        class="input-field"
        @keyup.enter="handleSend"
        @focus="isFocused = true"
        @blur="isFocused = false"
      />
      <div class="input-glow" :class="{ focused: isFocused }"></div>
    </div>
    <button class="send-button" @click="handleSend" :disabled="!inputText.trim()">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="7" stroke="currentColor" stroke-width="1.5" opacity="0.8"/>
        <path
          d="M12 12L17 7"
          stroke="currentColor"
          stroke-width="1.7"
          stroke-linecap="round"
        />
        <path
          d="M12 5V3M19 12H21M12 21V19M3 12H5"
          stroke="currentColor"
          stroke-width="1.3"
          stroke-linecap="round"
          opacity="0.6"
        />
      </svg>
      <div class="button-shine"></div>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send'])

const inputText = ref('')
const isFocused = ref(false)

const handleSend = () => {
  if (inputText.value.trim()) {
    emit('send', inputText.value)
    inputText.value = ''
  }
}
</script>

<style scoped>
.input-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem 1.1rem;
  background: rgba(32, 44, 86, 0.88);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 18px;
  box-shadow:
    0 12px 34px rgba(6, 10, 24, 0.58),
    0 0 0 1px rgba(132, 206, 255, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(132, 206, 255, 0.22);
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.input-field {
  width: 100%;
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-family: inherit;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(38, 52, 98, 0.7);
  color: #fbfdff;
  letter-spacing: -0.01em;
  border: 1px solid rgba(132, 206, 255, 0.24);
}

.input-field:focus {
  background: rgba(38, 52, 98, 0.95);
  border-color: rgba(132, 206, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(132, 206, 255, 0.2);
}

.input-field::placeholder {
  color: #c0cee9;
  font-weight: 400;
}

.input-glow {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #8ce6ff, transparent);
  opacity: 0;
  transition: opacity 0.3s;
  box-shadow: 0 0 8px rgba(140, 230, 255, 0.38);
}

.input-glow.focused {
  opacity: 1;
}

.send-button {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8ce6ff, #7aa5ff);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #071326;
  padding: 0;
  flex-shrink: 0;
  box-shadow:
    0 4px 14px rgba(140, 230, 255, 0.45),
    0 0 24px rgba(140, 230, 255, 0.35);
  overflow: hidden;
}

.send-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.35), transparent);
  transition: left 0.5s;
}

.send-button:hover:not(:disabled)::before {
  left: 100%;
}

.send-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #9cf0ff, #87b2ff);
  transform: translateY(-2px);
  box-shadow:
    0 6px 20px rgba(140, 230, 255, 0.55),
    0 0 34px rgba(140, 230, 255, 0.4);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow:
    0 4px 12px rgba(140, 230, 255, 0.45),
    0 0 22px rgba(140, 230, 255, 0.32);
}

.send-button:disabled {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.2);
  cursor: not-allowed;
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.send-button svg {
  width: 18px;
  height: 18px;
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.3));
}

.button-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.send-button:hover:not(:disabled) .button-shine {
  opacity: 1;
}
</style>
