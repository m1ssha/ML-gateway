<script setup>
import { computed } from 'vue'
import { formatPercent } from '@/utils/formatters'

const props = defineProps({
  risk: {
    type: Number,
    required: true
  }
})

const percentage = computed(() => {
  // We normalize to 1.0 for the bar, but it can go higher
  return Math.min(props.risk * 100, 100)
})

const barColor = computed(() => {
  if (props.risk >= 1.0) return 'bg-red-500'
  if (props.risk >= 0.5) return 'bg-orange-500'
  return 'bg-green-500'
})

const isCritical = computed(() => props.risk >= 0.8)
</script>

<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-1">
      <span class="text-xs font-medium text-slate-500">Накопительный риск сессии</span>
      <span :class="['text-xs font-bold', risk >= 0.8 ? 'text-red-600' : 'text-slate-700']">
        {{ risk.toFixed(2) }}
      </span>
    </div>
    <div class="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
      <div 
        class="h-full transition-all duration-500 ease-out"
        :class="[barColor, { 'animate-pulse': isCritical }]"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
  </div>
</template>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.animate-pulse {
  animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
