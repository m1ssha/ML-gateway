import api from './api'

export default {
  async sendMessage(sessionId, message) {
    const response = await api.post('/chat', {
      session_id: sessionId,
      message: message
    })
    return response.data
  }
}
