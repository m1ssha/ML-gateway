<script setup>
import { Shield, Plus, Lock } from 'lucide-vue-next'
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

const props = defineProps({
  sessionId: String,
  createdAt: String,
  isBlocked: Boolean
})

const emit = defineEmits(['new'])

const formatDate = (dateStr) => {
  if (!dateStr) return '...'
  try {
    return formatDistanceToNow(new Date(dateStr), { addSuffix: true, locale: ru })
  } catch (e) {
    return dateStr
  }
}
</script>

<template>
  <div class="session-info">
    <div class="session-status" :class="{ 'is-blocked': isBlocked }">
      <div class="status-icon-box">
        <Lock v-if="isBlocked" class="status-icon" />
        <Shield v-else class="status-icon" />
      </div>
      <div class="session-details">
        <div class="session-label">
          <span>Активная сессия</span>
          <span v-if="isBlocked" class="blocked-badge">Заблокирована</span>
        </div>
        <div class="session-meta">
          <code class="session-id">{{ sessionId?.slice(0, 8) }}</code>
          <span class="dot"></span>
          <span class="session-time">{{ formatDate(createdAt) }}</span>
        </div>
      </div>
    </div>

    <button
      @click="emit('new')"
      class="new-session-btn"
      title="Начать новую сессию"
    >
      <Plus class="btn-icon" />
      <span>Новая сессия</span>
    </button>
  </div>
</template>

<style scoped>
.session-info {
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

.session-status {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.status-icon-box {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-gray-50);
  border: 1px solid var(--color-gray-100);
  color: var(--color-gray-500);
}

.is-blocked .status-icon-box {
  background-color: #fff1f2;
  border-color: #fecaca;
  color: var(--color-danger);
}

.status-icon {
  width: 18px;
  height: 18px;
}

.session-details {
  display: flex;
  flex-direction: column;
}

.session-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-gray-400);
  letter-spacing: 0.05em;
}

.blocked-badge {
  background-color: var(--color-danger);
  color: var(--color-white);
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 0.6rem;
  font-weight: 800;
}

.session-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.session-id {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--color-gray-700);
  font-weight: 600;
}

.dot {
  width: 3px;
  height: 3px;
  background-color: var(--color-gray-300);
  border-radius: 50%;
}

.session-time {
  font-size: 0.75rem;
  color: var(--color-gray-500);
}

.new-session-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background-color: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-md);
  color: var(--color-gray-700);
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-session-btn:hover {
  background-color: var(--color-gray-50);
  border-color: var(--color-gray-300);
}

.btn-icon {
  width: 14px;
  height: 14px;
  color: var(--color-primary);
}
</style>
