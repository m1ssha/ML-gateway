<script setup>
import { computed } from 'vue'
import { formatPercent } from '@/utils/formatters'

const props = defineProps({
  risk: {
    type: Number,
    default: 0
  }
})

const safeRisk = computed(() => props.risk || 0)

const percentage = computed(() => Math.min(safeRisk.value * 100, 100))

const isCritical = computed(() => safeRisk.value >= 0.8)
</script>

<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-1.5">
      <div class="flex items-center space-x-2">
        <span class="text-xs font-medium text-stone-500">Накопительный риск сессии</span>
        <div class="hidden sm:flex items-center space-x-3 text-[9px] text-stone-300 font-mono">
          <span>0</span>
          <span class="flex-1 border-t border-stone-200 mx-1"></span>
          <span>0.5</span>
          <span class="flex-1 border-t border-stone-200 mx-1"></span>
          <span>1.0</span>
        </div>
      </div>
      <span :class="['text-xs font-mono font-bold', safeRisk >= 0.8 ? 'text-red-600' : 'text-stone-600']">
        {{ safeRisk.toFixed(2) }}
      </span>
    </div>
    <div class="relative h-2.5 w-full bg-stone-200 rounded-full overflow-hidden">
      <div
        class="absolute inset-0 bg-gradient-to-r from-green-400 via-amber-400 to-red-500 opacity-20"
      ></div>
      <div
        class="relative h-full transition-all duration-700 ease-out rounded-full"
        :class="{
          'bg-gradient-to-r from-green-500 via-amber-500 to-red-500': isCritical,
          'bg-gradient-to-r from-green-400 via-amber-400 to-red-400': !isCritical,
          'animate-glow': isCritical
        }"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
    <div class="flex justify-between mt-0.5">
      <span class="text-[9px] text-stone-300 font-mono">0</span>
      <span class="text-[9px] text-stone-300 font-mono">0.5</span>
      <span class="text-[9px] text-stone-300 font-mono">1.0</span>
    </div>
  </div>
</template>