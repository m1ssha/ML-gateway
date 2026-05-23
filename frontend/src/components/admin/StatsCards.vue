<script setup>
import { ShieldCheck, ShieldAlert, BarChart3, Users } from 'lucide-vue-next'

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({
      total_requests: 0,
      blocked_requests: 0,
      avg_risk_score: 0,
      active_sessions: 0
    })
  }
})
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Total Requests -->
    <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
      <div class="bg-blue-50 p-3 rounded-lg text-blue-600">
        <BarChart3 class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Всего запросов</p>
        <p class="text-2xl font-bold text-slate-900">{{ stats.total_requests }}</p>
      </div>
    </div>

    <!-- Blocked -->
    <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
      <div class="bg-red-50 p-3 rounded-lg text-red-600">
        <ShieldAlert class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Заблокировано</p>
        <p class="text-2xl font-bold text-slate-900">{{ stats.blocked_requests }}</p>
      </div>
    </div>

    <!-- Avg Risk -->
    <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
      <div class="bg-orange-50 p-3 rounded-lg text-orange-600">
        <ShieldCheck class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Средний риск</p>
        <p class="text-2xl font-bold text-slate-900">{{ (stats.avg_risk_score || 0).toFixed(2) }}</p>
      </div>
    </div>

    <!-- Active Sessions -->
    <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
      <div class="bg-green-50 p-3 rounded-lg text-green-600">
        <Users class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">Активных сессий</p>
        <p class="text-2xl font-bold text-slate-900">{{ stats.active_sessions }}</p>
      </div>
    </div>
  </div>
</template>
