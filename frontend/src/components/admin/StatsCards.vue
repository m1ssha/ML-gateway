<script setup>
import { ref, watch, onMounted } from 'vue'
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

const animated = ref({
  total_requests: 0,
  blocked_requests: 0,
  active_sessions: 0,
  avg_risk_score: 0
})

const animateValue = (key, targetValue, duration = 600) => {
  const isFloat = key === 'avg_risk_score'
  const startValue = animated.value[key]
  const diff = targetValue - startValue
  const startTime = performance.now()

  const step = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)

    animated.value[key] = isFloat
      ? parseFloat((startValue + diff * eased).toFixed(2))
      : Math.round(startValue + diff * eased)

    if (progress < 1) {
      requestAnimationFrame(step)
    }
  }

  requestAnimationFrame(step)
}

watch(() => props.stats.total_requests, (v) => animateValue('total_requests', v || 0))
watch(() => props.stats.blocked_requests, (v) => animateValue('blocked_requests', v || 0))
watch(() => props.stats.active_sessions, (v) => animateValue('active_sessions', v || 0))
watch(() => props.stats.avg_risk_score, (v) => animateValue('avg_risk_score', v || 0))

onMounted(() => {
  animated.value.total_requests = props.stats.total_requests || 0
  animated.value.blocked_requests = props.stats.blocked_requests || 0
  animated.value.active_sessions = props.stats.active_sessions || 0
  animated.value.avg_risk_score = props.stats.avg_risk_score || 0
})
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100 flex items-center space-x-4">
      <div class="bg-emerald-50 p-3 rounded-lg text-emerald-600">
        <BarChart3 class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-stone-500 uppercase tracking-wider">Всего запросов</p>
        <p class="text-2xl font-bold text-stone-800 font-mono tabular-nums">{{ animated.total_requests }}</p>
      </div>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100 flex items-center space-x-4">
      <div class="bg-red-50 p-3 rounded-lg text-red-600">
        <ShieldAlert class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-stone-500 uppercase tracking-wider">Заблокировано</p>
        <p class="text-2xl font-bold text-stone-800 font-mono tabular-nums">{{ animated.blocked_requests }}</p>
      </div>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100 flex items-center space-x-4">
      <div class="bg-amber-50 p-3 rounded-lg text-amber-600">
        <ShieldCheck class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-stone-500 uppercase tracking-wider">Средний риск</p>
        <p class="text-2xl font-bold text-stone-800 font-mono tabular-nums">{{ animated.avg_risk_score }}</p>
      </div>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-stone-100 flex items-center space-x-4">
      <div class="bg-blue-50 p-3 rounded-lg text-blue-600">
        <Users class="w-6 h-6" />
      </div>
      <div>
        <p class="text-xs font-medium text-stone-500 uppercase tracking-wider">Активных сессий</p>
        <p class="text-2xl font-bold text-stone-800 font-mono tabular-nums">{{ animated.active_sessions }}</p>
      </div>
    </div>
  </div>
</template>