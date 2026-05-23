<script setup>
import { computed } from 'vue'
import { formatPercent } from '@/utils/formatters'

const props = defineProps({
  level: {
    type: String,
    default: 'low'
  },
  score: {
    type: Number,
    required: false
  }
})

const badgeStyle = computed(() => {
  if (props.level === 'high') return { color: 'var(--color-risk-high)', borderColor: 'var(--color-risk-high)', backgroundColor: '#fff1f2' }
  if (props.level === 'medium') return { color: 'var(--color-risk-medium)', borderColor: 'var(--color-risk-medium)', backgroundColor: '#fffbeb' }
  return { color: 'var(--color-risk-low)', borderColor: 'var(--color-risk-low)', backgroundColor: '#f0fdf4' }
})

const label = computed(() => {
  if (props.level === 'high') return 'HIGH RISK'
  if (props.level === 'medium') return 'MEDIUM RISK'
  return 'LOW RISK'
})
</script>

<template>
  <div class="risk-badge" :style="badgeStyle">
    <span class="badge-label">{{ label }}</span>
    <span v-if="score !== undefined" class="badge-score">{{ formatPercent(score) }}</span>
  </div>
</template>

<style scoped>
.risk-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 1px var(--space-2);
  border: 1px solid;
  border-radius: 4px;
  font-size: 0.6rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  line-height: 1;
}

.badge-label {
  white-space: nowrap;
}

.badge-score {
  opacity: 0.7;
  font-family: var(--font-mono);
}
</style>
