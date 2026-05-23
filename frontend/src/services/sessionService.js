import api from './api'

export default {
  async createSession() {
    const response = await api.post('/sessions')
    return response.data
  },
  
  async getSessionHistory(sessionId) {
    const response = await api.get(`/sessions/${sessionId}/history`)
    return response.data
  }
}
