<script setup>
import { computed } from 'vue'
import { User, Bot, ShieldAlert, AlertTriangle } from 'lucide-vue-next'
import RiskBadge from '@/components/risk/RiskBadge.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  showRisk: {
    type: Boolean,
    default: true
  }
})

const isUser = computed(() => props.message.role === 'user')
const isBlocked = computed(() => props.message.is_blocked)
</script>

<template>
  <div class="message-row" :class="[message.role, { 'is-blocked': isBlocked }]">
    <div class="message-inner">
      <div class="message-avatar">
        <div class="avatar-box">
          <User v-if="isUser" class="avatar-icon" />
          <Bot v-else class="avatar-icon" />
        </div>
      </div>
      
      <div class="message-content">
        <div class="message-header">
          <span class="role-name">{{ isUser ? 'User' : 'Assistant' }}</span>
          <div v-if="isBlocked" class="blocked-indicator">
            <ShieldAlert class="indicator-icon" />
            <span>Blocked</span>
          </div>
        </div>

        <div class="message-text">
          {{ message.content }}
        </div>

        <div v-if="!isUser && showRisk" class="message-footer">
          <div class="security-info">
            <span class="security-label">Security Scan:</span>
            <RiskBadge :level="message.risk_level" />
          </div>
          <div v-if="isBlocked" class="policy-alert">
            <AlertTriangle class="alert-icon" />
            <span>Policy Violation Detected</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-row {
  width: 100%;
  padding: var(--space-8) var(--space-6);
  border-bottom: 1px solid var(--color-gray-50);
}

.message-row.user {
  background-color: var(--color-white);
}

.message-row.assistant {
  background-color: var(--color-gray-50);
}

.message-row.is-blocked {
  background-color: #fff1f2; /* Light red */
}

.message-inner {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  gap: var(--space-6);
}

.message-avatar {
  flex-shrink: 0;
}

.avatar-box {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user .avatar-box {
  background-color: var(--color-gray-800);
  color: var(--color-white);
}

.assistant .avatar-box {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.avatar-icon {
  width: 18px;
  height: 18px;
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.message-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-1);
}

.role-name {
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--color-gray-900);
}

.blocked-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--color-danger);
  letter-spacing: 0.05em;
}

.indicator-icon {
  width: 14px;
  height: 14px;
}

.message-text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-gray-800);
  white-space: pre-wrap;
  word-break: break-word;
}

.message-footer {
  margin-top: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.security-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.security-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-gray-400);
  letter-spacing: 0.05em;
}

.policy-alert {
  display: flex;
  align-items: center;
  gap: var(--space-1.5);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-danger);
}

.alert-icon {
  width: 14px;
  height: 14px;
}
</style>
