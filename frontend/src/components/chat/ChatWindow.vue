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
  <div class="flex flex-col h-full w-full glass-panel rounded-3xl overflow-hidden relative shadow-2xl border-white/50">
    <!-- Top Session Info -->
    <div class="z-20">
      <SessionPanel
        :session-id="sessionStore.currentSessionId"
        :created-at="sessionStore.createdAt"
        :is-blocked="sessionStore.isBlocked"
        @new="createNewSession"
      />
      <div class="px-6 py-1">
        <CumulativeRiskBar :risk="sessionStore.cumulativeRisk" />
      </div>
    </div>

    <!-- Message Area -->
    <div class="flex-1 overflow-hidden relative">
      <MessageList
        :messages="chatStore.messages"
        :is-loading="chatStore.isLoading"
        :show-risk="showRiskDetails"
      />
    </div>

    <!-- Input Area -->
    <div class="p-6 pt-2 bg-white/30 backdrop-blur-md border-t border-white/20">
      <MessageInput
        :disabled="isInputDisabled"
        @send="handleSendMessage"
      />
    </div>
  </div>
</template>
