<script setup>
import { computed } from 'vue'
import { getRiskBgColor } from '@/utils/riskLevels'
import { formatPercent } from '@/utils/formatters'

const props = defineProps({
  score: {
    type: Number,
    required: true
  },
  showLabel: {
    type: Boolean,
    default: true
  }
})

const badgeClass = computed(() => {
  return `px-2 py-0.5 rounded-full text-xs font-medium ${getRiskBgColor(props.score)}`
})

const label = computed(() => {
  if (props.score >= 0.70) return 'Высокий риск'
  if (props.score >= 0.30) return 'Средний риск'
  return 'Низкий риск'
})
</script>

<template>
  <div :class="badgeClass">
    <span v-if="showLabel">{{ label }} </span>
    <span>{{ formatPercent(score) }}</span>
  </div>
</template>
