<script setup>
import { computed } from 'vue'
import { Plus, Copy, Check, Clock, ShieldX } from 'lucide-vue-next'
import { truncateId, formatFullDate } from '@/utils/formatters'
import { ref } from 'vue'

const props = defineProps({
  sessionId: String,
  createdAt: String,
  isBlocked: Boolean
})

const emit = defineEmits(['new'])

const copied = ref(false)

const copyId = () => {
  if (!props.sessionId) return
  navigator.clipboard.writeText(props.sessionId)
  copied.value = true
  setTimeout(() => copied.value = false, 2000)
}
</script>

<template>
  <div class="p-4 border-b border-stone-100 bg-white">
    <div class="flex items-center justify-between">
      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <span class="text-xs font-semibold text-stone-400 uppercase tracking-widest">Сессия</span>
          <div class="flex items-center bg-stone-100 px-2.5 py-0.5 rounded text-[10px] font-mono text-stone-600">
            <span>{{ truncateId(sessionId) }}</span>
            <button @click="copyId" class="ml-1.5 hover:text-emerald-600 transition-colors">
              <Check v-if="copied" class="w-3 h-3 text-green-600" />
              <Copy v-else class="w-3 h-3" />
            </button>
          </div>
        </div>
        <div v-if="createdAt" class="flex items-center mt-1 text-[10px] text-stone-400">
          <Clock class="w-3 h-3 mr-1" />
          <span>{{ formatFullDate(createdAt) }}</span>
        </div>
      </div>

      <button
        @click="emit('new')"
        class="group flex items-center space-x-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-lg text-xs font-semibold hover:bg-emerald-100 transition-colors"
      >
        <Plus class="w-4 h-4 transition-transform duration-300 group-hover:rotate-90" />
        <span>Новый диалог</span>
      </button>
    </div>

    <div v-if="isBlocked" class="mt-3 flex items-center space-x-2 p-2.5 bg-red-50 rounded-lg border border-red-100">
      <ShieldX class="w-4 h-4 text-red-500 flex-shrink-0" />
      <span class="text-xs font-bold text-red-700 uppercase tracking-tight">
        Сеанс заблокирован из-за подозрительной активности
      </span>
    </div>
  </div>
</template>