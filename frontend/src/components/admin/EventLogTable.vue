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
    case 'passed': return 'status-passed'
    case 'reviewed': return 'status-reviewed'
    case 'blocked': return 'status-blocked'
    default: return 'status-unknown'
  }
}
</script>

<template>
  <div class="table-wrapper">
    <table class="data-table">
      <thead>
        <tr>
          <th>Время</th>
          <th>Сессия</th>
          <th>Роль</th>
          <th>Содержимое</th>
          <th>Риск</th>
          <th>Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td class="cell-time">
            {{ formatFullDate(log.created_at) }}
          </td>
          <td class="cell-id">
            <code>{{ truncateId(log.session_id) }}</code>
          </td>
          <td class="cell-role">
            <span class="role-badge" :class="log.role">
              {{ log.role === 'user' ? 'польз.' : 'ассист.' }}
            </span>
          </td>
          <td class="cell-content">
            <div class="content-truncate" :title="log.content">
              {{ log.content }}
            </div>
          </td>
          <td class="cell-risk">
            <RiskBadge v-if="log.risk_score !== undefined" :level="log.risk_score >= 0.7 ? 'high' : (log.risk_score >= 0.3 ? 'medium' : 'low')" :score="log.risk_score" />
            <span v-else class="empty-val">—</span>
          </td>
          <td class="cell-status">
            <span class="decision-badge" :class="getDecisionClass(log.decision)">
              {{ log.decision === 'passed' ? 'ПРОШЛО' : (log.decision === 'blocked' ? 'БЛОК' : (log.decision === 'reviewed' ? 'ОБЗОР' : 'Н/Д')) }}
            </span>
          </td>
        </tr>
        <tr v-if="logs.length === 0">
          <td colspan="6" class="empty-table">
            Системные события не зарегистрированы.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
  text-align: left;
}

.data-table th {
  padding: var(--space-4) var(--space-6);
  background-color: var(--color-gray-50);
  border-bottom: 1px solid var(--color-gray-200);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-gray-500);
  font-size: 0.65rem;
}

.data-table td {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-gray-100);
  color: var(--color-gray-700);
  vertical-align: middle;
}

.data-table tbody tr:hover {
  background-color: var(--color-gray-50);
}

.cell-time {
  white-space: nowrap;
  color: var(--color-gray-500);
  font-variant-numeric: tabular-nums;
}

.cell-id code {
  font-family: var(--font-mono);
  background-color: var(--color-gray-100);
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.75rem;
  color: var(--color-gray-600);
}

.role-badge {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
}

.role-badge.user { background-color: #ecfdf5; color: #059669; }
.role-badge.assistant { background-color: #f5f3ff; color: #7c3aed; }

.content-truncate {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-gray-600);
}

.empty-val {
  color: var(--color-gray-200);
}

.decision-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.status-passed { background-color: var(--color-success); color: var(--color-white); }
.status-reviewed { background-color: var(--color-warning); color: var(--color-white); }
.status-blocked { background-color: var(--color-danger); color: var(--color-white); }
.status-unknown { background-color: var(--color-gray-100); color: var(--color-gray-500); }

.empty-table {
  padding: var(--space-12);
  text-align: center;
  color: var(--color-gray-400);
}
</style>
