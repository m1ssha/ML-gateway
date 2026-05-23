<script setup>
import { Shield, Plus, Lock, Calendar } from 'lucide-vue-next'
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
  <div class="px-6 py-4 flex items-center justify-between border-b border-white/20 bg-white/10 backdrop-blur-sm">
    <div class="flex items-center space-x-4">
      <div 
        class="w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-500"
        :class="isBlocked ? 'bg-rose-500/10 text-rose-500 border border-rose-500/20' : 'bg-indigo-500/10 text-indigo-600 border border-indigo-500/20'"
      >
        <Lock v-if="isBlocked" class="w-5 h-5" />
        <Shield v-else class="w-5 h-5" />
      </div>
      
      <div class="flex flex-col">
        <div class="flex items-center space-x-2">
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em]">Active Session</span>
          <div v-if="isBlocked" class="px-1.5 py-0.5 rounded bg-rose-500 text-white text-[9px] font-black uppercase tracking-tighter">
            Locked
          </div>
        </div>
        <div class="flex items-center space-x-3 mt-0.5">
          <code class="text-xs font-mono font-semibold text-slate-700">
            {{ sessionId?.slice(0, 8) }}...
          </code>
          <div class="w-1 h-1 rounded-full bg-slate-300"></div>
          <div class="flex items-center space-x-1.5 text-slate-400">
            <Calendar class="w-3 h-3" />
            <span class="text-[11px] font-medium">{{ formatDate(createdAt) }}</span>
          </div>
        </div>
      </div>
    </div>

    <button
      @click="emit('new')"
      class="flex items-center space-x-2 px-4 py-2 rounded-xl bg-white/60 hover:bg-white border border-white/80 shadow-sm transition-all duration-300 group"
    >
      <Plus class="w-4 h-4 text-indigo-600 transition-transform duration-300 group-hover:rotate-90" />
      <span class="text-sm font-bold text-slate-700">New Session</span>
    </button>
  </div>
</template>
