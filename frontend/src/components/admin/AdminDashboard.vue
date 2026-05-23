<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RefreshCcw, Activity } from 'lucide-vue-next'
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
  <div class="h-full overflow-y-auto glass-panel rounded-3xl p-8 relative shadow-2xl border-white/50">
    <div class="max-w-7xl mx-auto space-y-10">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-indigo-600/10 rounded-2xl border border-indigo-600/20">
            <Activity class="w-6 h-6 text-indigo-600" />
          </div>
          <div>
            <h2 class="text-2xl font-extrabold text-slate-800 tracking-tight">Admin Console</h2>
            <p class="text-slate-400 text-sm font-medium">Gateway security monitoring & system analytics</p>
          </div>
        </div>

        <div class="flex items-center space-x-6">
          <label class="flex items-center space-x-3 text-[11px] font-bold text-slate-400 uppercase tracking-widest cursor-pointer group">
            <input 
              type="checkbox" 
              v-model="autoRefresh" 
              class="w-4 h-4 rounded-md border-slate-200 text-indigo-600 focus:ring-indigo-500/20 transition-all cursor-pointer"
            >
            <span class="group-hover:text-slate-600 transition-colors">Auto-refresh (10s)</span>
          </label>
          <button
            @click="fetchData"
            class="p-2.5 bg-white/60 backdrop-blur-md border border-white rounded-xl shadow-sm hover:bg-white hover:shadow-md transition-all active:scale-95"
            :disabled="isLoading"
          >
            <RefreshCcw class="w-4 h-4 text-slate-500" :class="{ 'animate-spin': isLoading }" />
          </button>
        </div>
      </div>

      <div class="space-y-6">
        <StatsCards :stats="stats" />
      </div>

      <div class="space-y-6">
        <div class="flex items-center space-x-3 px-2">
          <div class="w-1 h-6 bg-indigo-500 rounded-full"></div>
          <h3 class="text-lg font-bold text-slate-800 tracking-tight">System Event Log</h3>
        </div>
        <div class="glass-card rounded-2xl overflow-hidden border-white/40">
          <EventLogTable :logs="logs" />
        </div>
      </div>
    </div>
  </div>
</template>
