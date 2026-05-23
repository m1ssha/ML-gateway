<script setup>
import { computed } from 'vue'
import { User, Bot, AlertTriangle, ShieldCheck, ShieldAlert } from 'lucide-vue-next'
import RiskBadge from '@/components/risk/RiskBadge.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  showRisk: {
    type: Boolean,
    default: true
  }
})

const isUser = computed(() => props.message.role === 'user')
const isBlocked = computed(() => props.message.is_blocked)

const containerClass = computed(() => {
  return [
    'flex w-full mb-6 px-6 transition-all duration-500',
    isUser.value ? 'justify-end' : 'justify-start'
  ]
})

const bubbleClass = computed(() => {
  if (isUser.value) {
    return 'bg-indigo-600 text-white rounded-2xl rounded-tr-none shadow-lg shadow-indigo-600/20'
  }
  return 'glass-card rounded-2xl rounded-tl-none border-white/60'
})
</script>

<template>
  <div :class="containerClass" class="message-transition">
    <div 
      class="flex max-w-[85%] sm:max-w-[75%]"
      :class="isUser ? 'flex-row-reverse' : 'flex-row'"
    >
      <!-- Avatar -->
      <div 
        class="flex-shrink-0 mt-1"
        :class="isUser ? 'ml-3' : 'mr-3'"
      >
        <div 
          class="w-8 h-8 rounded-xl flex items-center justify-center border transition-all duration-300"
          :class="isUser 
            ? 'bg-indigo-50 border-indigo-100 text-indigo-600' 
            : 'bg-white/80 border-slate-100 text-slate-500 shadow-sm'"
        >
          <User v-if="isUser" class="w-4 h-4" />
          <Bot v-else class="w-4 h-4" />
        </div>
      </div>

      <!-- Content -->
      <div class="flex flex-col" :class="isUser ? 'items-end' : 'items-start'">
        <div :class="[bubbleClass, 'px-5 py-3.5 relative']">
          <p class="text-[15px] leading-relaxed whitespace-pre-wrap font-medium">
            {{ message.content }}
          </p>

          <!-- Blocked Overlay/Icon -->
          <div 
            v-if="isBlocked" 
            class="absolute -top-2 -right-2 bg-rose-500 text-white p-1 rounded-full shadow-lg border-2 border-white"
          >
            <ShieldAlert class="w-3.5 h-3.5" />
          </div>
        </div>

        <!-- Meta Info (Risk, Timestamp) -->
        <div 
          v-if="!isUser && showRisk" 
          class="flex items-center space-x-3 mt-2 px-1"
        >
          <div class="flex items-center space-x-1.5 bg-white/40 px-2 py-0.5 rounded-lg border border-white/60">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Security Scan</span>
            <RiskBadge :level="message.risk_level" />
          </div>
          
          <div v-if="isBlocked" class="flex items-center space-x-1 text-rose-500 font-bold text-[10px] uppercase tracking-wider">
            <AlertTriangle class="w-3 h-3" />
            <span>Policy Violation</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
