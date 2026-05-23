<script setup>
import { truncateId, formatFullDate } from '@/utils/formatters'
import RiskBadge from '@/components/risk/RiskBadge.vue'

const props = defineProps({
  logs: {
    type: Array,
    default: () => []
  }
})

const getRowBorderClass = (decision) => {
  switch (decision) {
    case 'passed': return 'border-l-emerald-400'
    case 'reviewed': return 'border-l-amber-400'
    case 'blocked': return 'border-l-red-400'
    default: return 'border-l-transparent'
  }
}

const getDecisionClass = (decision) => {
  switch (decision) {
    case 'passed': return 'text-emerald-600 bg-emerald-50'
    case 'reviewed': return 'text-amber-600 bg-amber-50'
    case 'blocked': return 'text-red-600 bg-red-50'
    default: return 'text-stone-500 bg-stone-50'
  }
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-stone-100 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-stone-50 border-b border-stone-100">
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Дата</th>
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Session ID</th>
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Роль</th>
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Содержимое</th>
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Риск</th>
            <th class="px-6 py-4 text-xs font-bold text-stone-400 uppercase tracking-wider">Статус</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-stone-50">
          <tr v-for="log in logs" :key="log.id" class="border-l-2 transition-colors hover:bg-stone-50/50" :class="getRowBorderClass(log.decision)">
            <td class="px-6 py-4 whitespace-nowrap text-xs text-stone-500">
              {{ formatFullDate(log.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap font-mono text-xs text-stone-400">
              {{ truncateId(log.session_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight"
                :class="log.role === 'user' ? 'text-emerald-600 bg-emerald-50' : 'text-violet-600 bg-violet-50'"
              >
                {{ log.role }}
              </span>
            </td>
            <td class="px-6 py-4">
              <p class="text-xs text-stone-600 line-clamp-1 max-w-xs">{{ log.content }}</p>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <RiskBadge v-if="log.risk_score !== undefined" :score="log.risk_score" :show-label="false" />
              <span v-else class="text-xs text-stone-300">—</span>
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
            <td colspan="6" class="px-6 py-12 text-center text-stone-400 text-sm">
              Нет записей в журнале
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>