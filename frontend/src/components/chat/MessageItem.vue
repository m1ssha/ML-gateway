<script setup>
import { computed } from 'vue'
import { CheckCircle2, User, Bot, ShieldCheck } from 'lucide-vue-next'
import { formatDateTime } from '@/utils/formatters'
import RiskBadge from '@/components/risk/RiskBadge.vue'
import BlockedMessage from './BlockedMessage.vue'

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
const isSystem = computed(() => props.message.role === 'system')
const isAssistant = computed(() => props.message.role === 'assistant')
const isBlocked = computed(() => props.message.decision === 'blocked')
const isReviewed = computed(() => props.message.decision === 'reviewed')

const containerClass = computed(() => [
  'flex w-full mb-6',
  isUser.value ? 'justify-end' : 'justify-start'
])

const bubbleClass = computed(() => [
  'relative max-w-[85%] px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed',
  isUser.value 
    ? 'bg-blue-600 text-white rounded-tr-none' 
    : 'bg-white text-slate-800 border border-slate-100 rounded-tl-none'
])
</script>

<template>
  <div :class="containerClass">
    <!-- Assistant/System Avatar -->
    <div v-if="!isUser" class="mr-3 flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
        <Bot v-if="isAssistant" class="w-5 h-5 text-blue-600" />
        <ShieldCheck v-else class="w-5 h-5 text-red-500" />
      </div>
    </div>

    <div class="flex flex-col" :class="isUser ? 'items-end' : 'items-start'">
      <!-- Message Content -->
      <div v-if="isBlocked || isSystem">
        <BlockedMessage :risk-score="message.risk_score" :show-details="showRisk" />
      </div>
      
      <div v-else :class="bubbleClass">
        <p class="whitespace-pre-wrap">{{ message.content }}</p>
        
        <!-- Status Indicator for Assistant -->
        <div v-if="isAssistant && isReviewed" class="mt-2 flex items-center text-[10px] font-medium text-orange-600 uppercase tracking-wider">
          <CheckCircle2 class="w-3 h-3 mr-1" />
          Проверено шлюзом
        </div>
      </div>

      <!-- Metadata (Time, Risk) -->
      <div class="mt-1 flex items-center space-x-2 text-[10px] text-slate-400">
        <span>{{ formatDateTime(message.created_at) }}</span>
        
        <template v-if="!isUser && !isBlocked && showRisk && message.risk_score !== undefined">
          <span>•</span>
          <RiskBadge :score="message.risk_score" :show-label="false" />
        </template>
      </div>
    </div>

    <!-- User Avatar -->
    <div v-if="isUser" class="ml-3 flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center border border-blue-200">
        <User class="w-5 h-5 text-blue-600" />
      </div>
    </div>
  </div>
</template>
