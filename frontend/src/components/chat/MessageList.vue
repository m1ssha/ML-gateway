<script setup>
import { useAutoScroll } from '@/composables/useAutoScroll'
import MessageItem from './MessageItem.vue'
import TypingIndicator from './TypingIndicator.vue'
import { MessageSquare } from 'lucide-vue-next'

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
    class="message-list-container"
  >
    <div v-if="messages.length === 0 && !isLoading" class="empty-state">
      <div class="empty-icon-wrapper">
        <MessageSquare class="empty-icon" />
      </div>
      <div class="empty-text">
        <h3>История сообщений пуста</h3>
        <p>Отправьте сообщение, чтобы начать новую сессию</p>
      </div>
    </div>

    <div class="messages-stack">
      <MessageItem
        v-for="(msg, idx) in messages"
        :key="msg.id"
        :message="msg"
        :show-risk="showRisk"
        :index="idx"
      />

      <div v-if="isLoading" class="typing-container">
        <div class="typing-avatar">
          <div class="avatar-bot small animate-pulse"></div>
        </div>
        <TypingIndicator />
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-list-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-10);
  text-align: center;
}

.empty-icon-wrapper {
  width: 64px;
  height: 64px;
  background-color: var(--color-gray-50);
  border: 1px solid var(--color-gray-100);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.empty-icon {
  width: 32px;
  height: 32px;
  color: var(--color-gray-300);
}

.empty-text h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-gray-700);
  margin-bottom: var(--space-2);
}

.empty-text p {
  font-size: 0.875rem;
  color: var(--color-gray-400);
  max-width: 320px;
}

.messages-stack {
  display: flex;
  flex-direction: column;
}

.typing-container {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6) var(--space-12);
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.typing-avatar {
  flex-shrink: 0;
}

.avatar-bot.small {
  width: 24px;
  height: 24px;
  background-color: var(--color-primary);
  border-radius: var(--border-radius-sm);
  opacity: 0.5;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.2; }
}
</style>
