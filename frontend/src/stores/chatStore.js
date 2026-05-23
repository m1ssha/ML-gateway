import { defineStore } from 'pinia'
import chatService from '@/services/chatService'
import sessionService from '@/services/sessionService'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [],
    isLoading: false,
    error: null,
    lastRiskScore: 0.0
  }),
  
  getters: {
    messagesByStep: (state) => {
      // Grouping logic if needed, but usually just returning messages is enough
      return state.messages
    }
  },
  
  actions: {
    addUserMessage(content) {
      this.messages.push({
        id: Date.now().toString(),
        role: 'user',
        content,
        created_at: new Date().toISOString()
      })
    },
    
    async sendMessage(sessionId, content) {
      this.isLoading = true
      this.error = null
      
      // Optimistic UI: user message already added by component
      
      try {
        const data = await chatService.sendMessage(sessionId, content)
        this.lastRiskScore = data.risk_score
        
        this.messages.push({
          id: Date.now().toString() + '-ai',
          role: data.status === 'blocked' ? 'system' : 'assistant',
          content: data.reply,
          risk_score: data.risk_score,
          is_attack: data.is_attack,
          decision: data.status,
          created_at: new Date().toISOString()
        })
        
        return data
      } catch (error) {
        this.error = 'Ошибка отправки сообщения'
        console.error(error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async loadHistory(sessionId) {
      this.isLoading = true
      try {
        const data = await sessionService.getSessionHistory(sessionId)
        this.messages = data.messages
        this.lastRiskScore = this.messages.length > 0 ? this.messages[this.messages.length - 1].risk_score : 0
      } catch (error) {
        this.error = 'Ошибка загрузки истории'
        console.error(error)
      } finally {
        this.isLoading = false
      }
    },
    
    clearMessages() {
      this.messages = []
      this.lastRiskScore = 0
    }
  }
})
