<script setup>
import { onMounted, ref, computed } from 'vue'
import { useSessionStore } from '@/stores/sessionStore'
import { useChatStore } from '@/stores/chatStore'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'
import SessionPanel from '@/components/session/SessionPanel.vue'
import CumulativeRiskBar from '@/components/risk/CumulativeRiskBar.vue'

const sessionStore = useSessionStore()
const chatStore = useChatStore()

const showRiskDetails = ref(import.meta.env.VITE_SHOW_RISK_DETAILS === 'true' || true)

onMounted(async () => {
  if (sessionStore.currentSessionId) {
    try {
      await sessionStore.loadSession(sessionStore.currentSessionId)
      await chatStore.loadHistory(sessionStore.currentSessionId)
    } catch (e) {
      console.error('Session expired or not found, creating new...')
      await createNewSession()
    }
  } else {
    await createNewSession()
  }
})

const createNewSession = async () => {
  await sessionStore.createSession()
  chatStore.clearMessages()
}

const handleSendMessage = async (text) => {
  if (!sessionStore.currentSessionId) {
    await createNewSession()
  }

  chatStore.addUserMessage(text)

  try {
    const response = await chatStore.sendMessage(sessionStore.currentSessionId, text)
    sessionStore.updateFromChatResponse(response)
    await sessionStore.loadSession(sessionStore.currentSessionId)
  } catch (error) {
    console.error('Send error:', error)
  }
}

const isInputDisabled = computed(() => {
  return chatStore.isLoading || sessionStore.isBlocked
})
</script>

<template>
  <div class="chat-window">
    <header class="chat-header">
      <div class="header-content">
        <SessionPanel
          :session-id="sessionStore.currentSessionId"
          :created-at="sessionStore.createdAt"
          :is-blocked="sessionStore.isBlocked"
          @new="createNewSession"
        />
        <div class="risk-monitor">
          <span class="risk-label">Уровень риска</span>
          <CumulativeRiskBar :risk="sessionStore.cumulativeRisk" />
        </div>
      </div>
    </header>

    <div class="chat-main">
      <div class="chat-scroll-area">
        <MessageList
          :messages="chatStore.messages"
          :is-loading="chatStore.isLoading"
          :show-risk="showRiskDetails"
        />
      </div>
    </div>

    <footer class="chat-footer">
      <div class="footer-content">
        <MessageInput
          :disabled="isInputDisabled"
          @send="handleSendMessage"
        />
        <div class="footer-note" v-if="sessionStore.isBlocked">
          Эта сессия была заблокирована из-за нарушения политики безопасности.
        </div>
        <div class="footer-note" v-else>
          Шлюз обеспечивает фильтрованный доступ к сервисам LLM.
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background-color: var(--color-white);
}

.chat-header {
  border-bottom: 1px solid var(--color-gray-100);
  padding: var(--space-4) var(--space-6);
  z-index: 10;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.risk-monitor {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  min-width: 200px;
}

.risk-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-gray-500);
}

.chat-main {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.chat-scroll-area {
  height: 100%;
  width: 100%;
  overflow-y: auto;
}

.chat-footer {
  padding: var(--space-4) var(--space-6) var(--space-8);
}

.footer-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer-note {
  font-size: 0.75rem;
  color: var(--color-gray-400);
  text-align: center;
}
</style>
