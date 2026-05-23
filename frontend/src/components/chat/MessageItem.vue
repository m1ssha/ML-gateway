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
  },
  index: {
    type: Number,
    default: 0
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
  'relative px-4 py-3 rounded-2xl shadow-sm text-sm leading-relaxed',
  isUser.value
    ? 'bg-emerald-600 text-white rounded-tr-none max-w-[70%]'
    : 'bg-white text-stone-700 border border-stone-100 rounded-tl-none max-w-[90%]'
])

const animationDelay = computed(() => `${props.index * 60}ms`)
</script>

<template>
  <div :class="containerClass" class="message-enter" :style="{ animationDelay }">
    <div v-if="!isUser" class="mr-3 flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-stone-100 flex items-center justify-center border border-stone-200">
        <Bot v-if="isAssistant" class="w-4 h-4 text-emerald-600" />
        <ShieldCheck v-else class="w-4 h-4 text-red-500" />
      </div>
    </div>

    <div class="flex flex-col" :class="isUser ? 'items-end' : 'items-start'">
      <div v-if="isBlocked || isSystem">
        <BlockedMessage :risk-score="message.risk_score" :show-details="showRisk" />
      </div>

      <div v-else :class="bubbleClass">
        <p class="whitespace-pre-wrap">{{ message.content }}</p>

        <div v-if="isAssistant && isReviewed" class="mt-2 flex items-center text-[10px] font-medium text-amber-600 uppercase tracking-wider">
          <CheckCircle2 class="w-3 h-3 mr-1" />
          Проверено шлюзом
        </div>
      </div>

      <div class="mt-1 flex items-center space-x-2 text-[10px] text-stone-400">
        <span>{{ formatDateTime(message.created_at) }}</span>

        <template v-if="!isUser && !isBlocked && showRisk && message.risk_score !== undefined">
          <span>·</span>
          <RiskBadge :score="message.risk_score" :show-label="false" />
        </template>
      </div>
    </div>

    <div v-if="isUser" class="ml-3 flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-emerald-50 flex items-center justify-center border border-emerald-200">
        <User class="w-4 h-4 text-emerald-600" />
      </div>
    </div>
  </div>
</template>