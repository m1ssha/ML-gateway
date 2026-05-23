<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RefreshCcw } from 'lucide-vue-next'
import adminService from '@/services/adminService'
import StatsCards from './StatsCards.vue'
import EventLogTable from './EventLogTable.vue'

const stats = ref({})
const logs = ref([])
const isLoading = ref(false)
const autoRefresh = ref(true)
let refreshInterval = null

const fetchData = async () => {
  isLoading.value = true
  try {
    const [statsData, logsData] = await Promise.all([
      adminService.getStats(),
      adminService.getLogs({ limit: 50 })
    ])
    stats.value = statsData
    logs.value = logsData
  } catch (error) {
    console.error('Failed to fetch admin data:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchData()
  refreshInterval = setInterval(() => {
    if (autoRefresh.value) fetchData()
  }, 10000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<template>
  <div class="h-full overflow-y-auto bg-slate-50 p-6">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-slate-900">Административная панель</h2>
          <p class="text-slate-500 text-sm mt-1">Мониторинг безопасности и статистика шлюза</p>
        </div>
        
        <div class="flex items-center space-x-4">
          <label class="flex items-center space-x-2 text-xs font-medium text-slate-500 cursor-pointer">
            <input type="checkbox" v-model="autoRefresh" class="rounded text-blue-600 focus:ring-blue-500">
            <span>Автообновление (10с)</span>
          </label>
          <button 
            @click="fetchData" 
            class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm hover:bg-slate-50 transition-colors"
            :disabled="isLoading"
          >
            <RefreshCcw class="w-4 h-4 text-slate-600" :class="{ 'animate-spin': isLoading }" />
          </button>
        </div>
      </div>

      <!-- Stats -->
      <StatsCards :stats="stats" />

      <!-- Logs Section -->
      <div class="space-y-4">
        <h3 class="text-lg font-bold text-slate-900">Журнал событий</h3>
        <EventLogTable :logs="logs" />
      </div>
    </div>
  </div>
</template>
