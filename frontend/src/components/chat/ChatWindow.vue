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
  <div class="flex flex-col h-full max-w-4xl mx-auto bg-white shadow-lg border-x border-stone-200">
    <SessionPanel
      :session-id="sessionStore.currentSessionId"
      :created-at="sessionStore.createdAt"
      :is-blocked="sessionStore.isBlocked"
      @new="createNewSession"
    />

    <div class="sticky top-0 z-10 px-4 py-2 bg-stone-50/90 backdrop-blur-sm border-b border-stone-100">
      <CumulativeRiskBar :risk="sessionStore.cumulativeRisk" />
    </div>

    <MessageList
      :messages="chatStore.messages"
      :is-loading="chatStore.isLoading"
      :show-risk="showRiskDetails"
    />

    <MessageInput
      :disabled="isInputDisabled"
      @send="handleSendMessage"
    />
  </div>
</template>