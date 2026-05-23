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
  <div class="admin-page">
    <header class="admin-header">
      <div class="header-main">
        <div class="page-title">
          <div class="title-icon-box">
            <Activity class="title-icon" />
          </div>
          <div class="title-text">
            <h1>Admin Console</h1>
            <p>Security monitoring and system analytics</p>
          </div>
        </div>

        <div class="header-actions">
          <label class="auto-refresh-toggle">
            <input 
              type="checkbox" 
              v-model="autoRefresh" 
              class="checkbox-input"
            >
            <span class="checkbox-label">Auto-refresh (10s)</span>
          </label>
          <button
            @click="fetchData"
            class="refresh-btn"
            :disabled="isLoading"
          >
            <RefreshCcw class="btn-icon" :class="{ 'is-spinning': isLoading }" />
            <span>Sync</span>
          </button>
        </div>
      </div>
    </header>

    <div class="admin-content">
      <section class="admin-section">
        <StatsCards :stats="stats" />
      </section>

      <section class="admin-section">
        <div class="section-header">
          <div class="accent-bar"></div>
          <h2>System Event Log</h2>
        </div>
        <div class="table-container">
          <EventLogTable :logs="logs" />
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  height: 100%;
  overflow-y: auto;
  background-color: var(--color-gray-50);
}

.admin-header {
  background-color: var(--color-white);
  border-bottom: 1px solid var(--color-gray-200);
  padding: var(--space-6) var(--space-8);
  position: sticky;
  top: 0;
  z-index: 20;
}

.header-main {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.title-icon-box {
  width: 44px;
  height: 44px;
  background-color: var(--color-gray-900);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
}

.title-icon {
  width: 20px;
  height: 20px;
}

.title-text h1 {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-gray-900);
  letter-spacing: -0.02em;
}

.title-text p {
  font-size: 0.8125rem;
  color: var(--color-gray-500);
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.auto-refresh-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  accent-color: var(--color-primary);
}

.checkbox-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background-color: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-md);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--color-gray-700);
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover:not(:disabled) {
  background-color: var(--color-gray-50);
  border-color: var(--color-gray-300);
}

.btn-icon {
  width: 14px;
  height: 14px;
}

.is-spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  gap: var(--space-10);
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.accent-bar {
  width: 4px;
  height: 24px;
  background-color: var(--color-primary);
  border-radius: 2px;
}

.section-header h2 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-gray-900);
}

.table-container {
  background-color: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
</style>
