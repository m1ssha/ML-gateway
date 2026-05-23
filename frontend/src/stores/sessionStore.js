import { defineStore } from 'pinia'
import sessionService from '@/services/sessionService'

export const useSessionStore = defineStore('session', {
  state: () => ({
    currentSessionId: localStorage.getItem('session_id') || null,
    createdAt: null,
    cumulativeRisk: 0.0,
    isBlocked: false,
    isLoading: false
  }),
  
  getters: {
    isActive: (state) => !!state.currentSessionId,
    riskLevel: (state) => {
      if (state.cumulativeRisk >= 1.0) return 'high'
      if (state.cumulativeRisk >= 0.5) return 'medium'
      return 'low'
    }
  },
  
  actions: {
    async createSession() {
      this.isLoading = true
      try {
        const data = await sessionService.createSession()
        this.currentSessionId = data.session_id
        this.createdAt = data.created_at
        this.cumulativeRisk = 0.0
        this.isBlocked = false
        localStorage.setItem('session_id', data.session_id)
        return data
      } catch (error) {
        console.error('Failed to create session:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async loadSession(sessionId) {
      this.isLoading = true
      try {
        const data = await sessionService.getSessionHistory(sessionId)
        this.currentSessionId = data.session_id
        this.cumulativeRisk = data.cumulative_risk
        this.isBlocked = data.is_blocked
        return data
      } catch (error) {
        console.error('Failed to load session:', error)
        // If session not found, clear it
        this.resetSession()
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    updateFromChatResponse(data) {
      // Assuming backend returns cumulative risk in chat response or we handle it here
      // Based on contracts, chat response has status/risk_score. 
      // We might need another way to get cumulative risk if not in chat response.
      // Let's assume we might need to refresh history or the backend provides it.
      // Actually, let's just update based on what we get.
      if (data.status === 'blocked') {
        this.isBlocked = true
      }
      // Note: Backend contract for /api/chat doesn't explicitly return cumulative_risk,
      // but it's good practice. If not, we'd need to fetch history.
    },
    
    resetSession() {
      this.currentSessionId = null
      this.createdAt = null
      this.cumulativeRisk = 0.0
      this.isBlocked = false
      localStorage.removeItem('session_id')
    }
  }
})
