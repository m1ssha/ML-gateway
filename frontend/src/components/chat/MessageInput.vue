<script setup>
import { ref } from 'vue'
import { Send, CornerDownLeft } from 'lucide-vue-next'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send'])
const message = ref('')

const handleSend = () => {
  if (message.value.trim() && !props.disabled) {
    emit('send', message.value)
    message.value = ''
  }
}
</script>

<template>
  <div class="relative group">
    <div class="glass-card rounded-2xl p-1.5 transition-all duration-300 group-focus-within:shadow-xl group-focus-within:shadow-indigo-600/5 group-focus-within:border-indigo-200">
      <div class="flex items-end space-x-2">
        <textarea
          v-model="message"
          rows="1"
          placeholder="Ask a question..."
          class="flex-1 bg-transparent border-0 focus:ring-0 text-[15px] py-3 px-4 resize-none max-h-32 min-h-[52px] placeholder:text-slate-400 font-medium"
          :disabled="disabled"
          @keydown.enter.prevent="handleSend"
        ></textarea>
        
        <button
          @click="handleSend"
          :disabled="disabled || !message.trim()"
          class="p-3 rounded-xl transition-all duration-300 flex items-center justify-center mb-1.5 mr-1.5 group/btn"
          :class="[
            message.trim() && !disabled
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20 scale-100'
              : 'bg-slate-100 text-slate-400 scale-95 opacity-50'
          ]"
        >
          <Send class="w-5 h-5 transition-transform duration-300 group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5" />
        </button>
      </div>
    </div>
    
    <!-- Keyboard Hint -->
    <div class="absolute -bottom-6 right-2 flex items-center space-x-1 opacity-0 group-focus-within:opacity-100 transition-opacity duration-500">
      <CornerDownLeft class="w-3 h-3 text-slate-400" />
      <span class="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Press Enter to send</span>
    </div>
  </div>
</template>
