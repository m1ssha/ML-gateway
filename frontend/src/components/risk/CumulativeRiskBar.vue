<script setup>
import { computed } from 'vue'
import { Shield, ShieldAlert, ShieldCheck } from 'lucide-vue-next'

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
  if (riskLevel.value === 'high') return 'Critical Risk'
  if (riskLevel.value === 'medium') return 'Elevated Risk'
  return 'Secure'
})

const colorClass = computed(() => {
  if (riskLevel.value === 'high') return 'bg-rose-500 shadow-rose-500/50'
  if (riskLevel.value === 'medium') return 'bg-amber-500 shadow-amber-500/50'
  return 'bg-emerald-500 shadow-emerald-500/50'
})
</script>

<template>
  <div class="flex items-center justify-between px-2 py-2">
    <div class="flex items-center space-x-3">
      <!-- Ambient Glow Indicator -->
      <div class="relative flex items-center justify-center">
        <div 
          class="w-2.5 h-2.5 rounded-full transition-all duration-1000 animate-pulse shadow-[0_0_12px_rgba(0,0,0,0.1)]"
          :class="colorClass"
        ></div>
        <div 
          class="absolute w-5 h-5 rounded-full opacity-20 transition-all duration-1000"
          :class="colorClass"
        ></div>
      </div>
      
      <div class="flex flex-col">
        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none">Security Status</span>
        <span 
          class="text-xs font-bold transition-colors duration-500"
          :class="{
            'text-rose-600': riskLevel === 'high',
            'text-amber-600': riskLevel === 'medium',
            'text-emerald-600': riskLevel === 'low'
          }"
        >
          {{ statusLabel }}
        </span>
      </div>
    </div>

    <!-- Minimal Risk Track -->
    <div class="w-32 h-1 bg-slate-100 rounded-full overflow-hidden relative">
      <div 
        class="absolute top-0 left-0 h-full transition-all duration-1000 ease-out"
        :class="colorClass"
        :style="{ width: `${risk * 100}%` }"
      ></div>
    </div>
  </div>
</template>
