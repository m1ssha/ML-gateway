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
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon-wrapper requests">
        <BarChart3 class="stat-icon" />
      </div>
      <div class="stat-info">
        <div class="stat-label">Total Requests</div>
        <div class="stat-value">{{ stats.total_requests || 0 }}</div>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon-wrapper blocked">
        <ShieldAlert class="stat-icon" />
      </div>
      <div class="stat-info">
        <div class="stat-label">Blocked</div>
        <div class="stat-value">{{ stats.blocked_requests || 0 }}</div>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon-wrapper risk">
        <ShieldCheck class="stat-icon" />
      </div>
      <div class="stat-info">
        <div class="stat-label">Avg. Risk</div>
        <div class="stat-value">{{ (stats.avg_risk_score || 0).toFixed(2) }}</div>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon-wrapper active">
        <Users class="stat-icon" />
      </div>
      <div class="stat-info">
        <div class="stat-label">Active Sessions</div>
        <div class="stat-value">{{ stats.active_sessions || 0 }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-4);
}

.stat-card {
  background-color: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  padding: var(--space-5);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  box-shadow: var(--shadow-sm);
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon {
  width: 24px;
  height: 24px;
}

.requests { background-color: #ecfdf5; color: #10b981; }
.blocked { background-color: #fff1f2; color: #ef4444; }
.risk { background-color: #fffbeb; color: #f59e0b; }
.active { background-color: #eff6ff; color: #3b82f6; }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--color-gray-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-gray-900);
  font-family: var(--font-mono);
  line-height: 1;
  margin-top: var(--space-1);
}
</style>
