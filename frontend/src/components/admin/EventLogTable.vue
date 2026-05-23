<script setup>
import { truncateId, formatFullDate } from '@/utils/formatters'
import RiskBadge from '@/components/risk/RiskBadge.vue'

const props = defineProps({
  logs: {
    type: Array,
    default: () => []
  }
})

const getDecisionClass = (decision) => {
  switch (decision) {
    case 'passed': return 'text-green-600 bg-green-50'
    case 'reviewed': return 'text-orange-600 bg-orange-50'
    case 'blocked': return 'text-red-600 bg-red-50'
    default: return 'text-slate-600 bg-slate-50'
  }
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50 border-b border-slate-100">
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Дата</th>
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Session ID</th>
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Роль</th>
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Содержимое</th>
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Риск</th>
            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Статус</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="log in logs" :key="log.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-500">
              {{ formatFullDate(log.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap font-mono text-xs text-slate-400">
              {{ truncateId(log.session_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight"
                :class="log.role === 'user' ? 'text-blue-600 bg-blue-50' : 'text-purple-600 bg-purple-50'"
              >
                {{ log.role }}
              </span>
            </td>
            <td class="px-6 py-4">
              <p class="text-xs text-slate-700 line-clamp-1 max-w-xs">{{ log.content }}</p>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <RiskBadge v-if="log.risk_score !== undefined" :score="log.risk_score" :show-label="false" />
              <span v-else class="text-xs text-slate-300">—</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight"
                :class="getDecisionClass(log.decision)"
              >
                {{ log.decision || 'N/A' }}
              </span>
            </td>
          </tr>
          <tr v-if="logs.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-slate-400 text-sm">
              Нет записей в журнале
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
