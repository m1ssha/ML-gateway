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
  <div class="flex flex-col space-y-2 p-4 bg-red-50 border border-red-100 rounded-xl max-w-[85%]">
    <div class="flex items-start space-x-3 text-red-700">
      <ShieldAlert class="w-5 h-5 mt-0.5 flex-shrink-0" />
      <div>
        <p class="font-semibold">Запрос заблокирован</p>
        <p class="text-sm mt-1">
          Ваш запрос не может быть обработан. Пожалуйста, переформулируйте сообщение или начните новый диалог.
        </p>
      </div>
    </div>
    
    <div v-if="showDetails && riskScore !== undefined" class="pt-2 border-t border-red-100 flex items-center justify-between">
      <span class="text-xs text-red-500 font-medium uppercase tracking-wider">Технические детали:</span>
      <RiskBadge :score="riskScore" :show-label="false" />
    </div>
  </div>
</template>
