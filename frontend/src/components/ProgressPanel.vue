<template>
  <div class="progress-panel">
    <div class="progress-header">
      <h2>进度面板</h2>
      <span>实时状态</span>
    </div>
    <div class="progress-list">
      <div
        v-for="item in items"
        :key="item.id"
        class="progress-item"
      >
        <div class="progress-icon">
          <span>Ai</span>
        </div>
        <div class="progress-info">
          <div class="progress-title">{{ item.title }}</div>
          <div class="progress-desc">{{ item.description }}</div>
        </div>
        <div class="progress-status">{{ item.status }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.progress-panel {
  flex: 0 0 20%;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  background: rgba(32, 44, 86, 0.9);
  border-radius: 20px;
  padding: 1.25rem 1rem;
  border: 1px solid rgba(132, 206, 255, 0.22);
  box-shadow:
    0 12px 32px rgba(6, 10, 24, 0.55),
    0 0 0 1px rgba(132, 206, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  min-width: 0;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  color: #f7fbff;
}

.progress-header h2 {
  font-size: 1rem;
  margin: 0;
}

.progress-header span {
  font-size: 0.75rem;
  color: rgba(199, 210, 254, 0.8);
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.progress-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.75rem;
  align-items: center;
  padding: 0.85rem;
  border-radius: 14px;
  background: rgba(42, 56, 104, 0.85);
  border: 1px solid rgba(132, 206, 255, 0.2);
}

.progress-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(140, 230, 255, 0.2);
  color: #081326;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.progress-info {
  min-width: 0;
}

.progress-title {
  font-size: 0.85rem;
  color: #f7fbff;
  margin-bottom: 0.15rem;
}

.progress-desc {
  font-size: 0.75rem;
  color: rgba(199, 210, 254, 0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-status {
  font-size: 0.75rem;
  color: #8ae7ff;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  border: 1px solid rgba(138, 231, 255, 0.6);
}
</style>

