<script setup>
import { computed } from 'vue'
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
  if (props.score < 0.30) return 'bg-green-50 text-green-700'
  if (props.score < 0.70) return 'bg-amber-50 text-amber-700'
  return 'bg-red-50 text-red-700'
})

const dotClass = computed(() => {
  if (props.score < 0.30) return 'bg-green-500'
  if (props.score < 0.70) return 'bg-amber-500'
  return 'bg-red-500'
})

const label = computed(() => {
  if (props.score >= 0.70) return 'Высокий риск'
  if (props.score >= 0.30) return 'Средний риск'
  return 'Низкий риск'
})
</script>

<template>
  <div class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium" :class="badgeClass">
    <span class="relative flex h-2 w-2">
      <span class="animate-pulse-dot absolute inline-flex h-full w-full rounded-full opacity-75" :class="dotClass"></span>
      <span class="relative inline-flex rounded-full h-2 w-2" :class="dotClass"></span>
    </span>
    <span v-if="showLabel">{{ label }} </span>
    <span>{{ formatPercent(score) }}</span>
  </div>
</template>