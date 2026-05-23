import api from './api'

export default {
  async getLogs(params = {}) {
    const response = await api.get('/admin/logs', { params })
    return response.data
  },
  
  async getStats() {
    const response = await api.get('/admin/stats')
    return response.data
  }
}
