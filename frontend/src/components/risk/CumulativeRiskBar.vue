<script setup>
import { computed } from 'vue'

const props = defineProps({
  risk: {
    type: Number,
    required: true
  }
})

const riskLevel = computed(() => {
  if (props.risk >= 0.7) return 'high'
  if (props.risk >= 0.3) return 'medium'
  return 'low'
})

const statusLabel = computed(() => {
  if (riskLevel.value === 'high') return 'CRITICAL'
  if (riskLevel.value === 'medium') return 'ELEVATED'
  return 'SECURE'
})

const colorVar = computed(() => {
  if (riskLevel.value === 'high') return 'var(--color-risk-high)'
  if (riskLevel.value === 'medium') return 'var(--color-risk-medium)'
  return 'var(--color-risk-low)'
})
</script>

<template>
  <div class="risk-bar-container">
    <div class="risk-track">
      <div 
        class="risk-fill" 
        :style="{ width: `${risk * 100}%`, backgroundColor: colorVar }"
      ></div>
    </div>
    <div class="risk-meta">
      <span class="status-indicator" :style="{ backgroundColor: colorVar }"></span>
      <span class="status-text" :style="{ color: colorVar }">{{ statusLabel }}</span>
      <span class="risk-value">{{ (risk * 100).toFixed(0) }}%</span>
    </div>
  </div>
</template>

<style scoped>
.risk-bar-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.risk-track {
  height: 4px;
  background-color: var(--color-gray-100);
  border-radius: 2px;
  overflow: hidden;
}

.risk-fill {
  height: 100%;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.risk-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.status-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-text {
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
}

.risk-value {
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--color-gray-400);
  margin-left: auto;
}
</style>
