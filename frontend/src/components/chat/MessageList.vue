<script setup>
import { useAutoScroll } from '@/composables/useAutoScroll'
import MessageItem from './MessageItem.vue'
import TypingIndicator from './TypingIndicator.vue'

const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  isLoading: Boolean,
  showRisk: Boolean
})

const { containerRef } = useAutoScroll(() => props.messages.length)
</script>

<template>
  <div 
    ref="containerRef"
    class="flex-1 overflow-y-auto p-4 space-y-2 scroll-smooth"
  >
    <div v-if="messages.length === 0 && !isLoading" class="h-full flex flex-col items-center justify-center text-slate-400 space-y-4">
      <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center border border-slate-100">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <div class="text-center">
        <p class="font-medium">История сообщений пуста</p>
        <p class="text-sm">Отправьте сообщение, чтобы начать диалог.</p>
      </div>
    </div>

    <MessageItem 
      v-for="msg in messages" 
      :key="msg.id" 
      :message="msg"
      :show-risk="showRisk"
    />

    <div v-if="isLoading" class="flex justify-start mb-6">
      <div class="mr-3 flex-shrink-0">
        <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-blue-600 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </div>
      </div>
      <TypingIndicator />
    </div>
  </div>
</template>
