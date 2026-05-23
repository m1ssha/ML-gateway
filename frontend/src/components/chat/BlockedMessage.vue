<script setup>
import { ShieldAlert } from 'lucide-vue-next'
import RiskBadge from '@/components/risk/RiskBadge.vue'

const props = defineProps({
  riskScore: Number,
  showDetails: {
    type: Boolean,
    default: true
  }
})
</script>

<template>
  <div class="relative flex flex-col max-w-[90%] bg-white rounded-2xl shadow-sm overflow-hidden border border-red-200">
    <div class="absolute inset-y-0 left-0 w-1 bg-red-500 rounded-l-full"></div>
    <div class="pl-5 p-4">
      <div class="flex items-start space-x-3 text-red-700">
        <ShieldAlert class="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div>
          <p class="font-semibold">Запрос заблокирован</p>
          <p class="text-sm mt-1 text-red-600/80">
            Ваш запрос не может быть обработан. Пожалуйста, переформулируйте сообщение или начните новый диалог.
          </p>
        </div>
      </div>

      <div v-if="showDetails && riskScore !== undefined" class="mt-3 pt-3 border-t border-red-100 flex items-center justify-between">
        <span class="text-xs text-red-400 font-medium uppercase tracking-wider">Технические детали:</span>
        <RiskBadge :score="riskScore" :show-label="false" />
      </div>
    </div>
  </div>
</template>