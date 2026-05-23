<script setup>
import { ref, watch, nextTick } from 'vue'
import { SendHorizontal } from 'lucide-vue-next'

const props = defineProps({
  disabled: Boolean,
  placeholder: {
    type: String,
    default: 'Введите сообщение...'
  }
})

const emit = defineEmits(['send'])
const text = ref('')
const textarea = ref(null)

const adjustHeight = () => {
  if (!textarea.value) return
  textarea.value.style.height = 'auto'
  textarea.value.style.height = Math.min(textarea.value.scrollHeight, 150) + 'px'
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

const send = () => {
  if (!text.value.trim() || props.disabled) return
  emit('send', text.value.trim())
  text.value = ''
  nextTick(() => {
    if (textarea.value) textarea.value.style.height = 'auto'
  })
}

watch(text, adjustHeight)
</script>

<template>
  <div class="p-4 bg-white border-t border-slate-100">
    <div 
      class="relative flex items-end space-x-2 bg-slate-50 border border-slate-200 rounded-2xl px-4 py-2 transition-all duration-200 focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100"
      :class="{ 'opacity-50 pointer-events-none': disabled }"
    >
      <textarea
        ref="textarea"
        v-model="text"
        rows="1"
        :placeholder="placeholder"
        class="w-full bg-transparent border-none focus:ring-0 resize-none py-1.5 text-sm text-slate-700 placeholder:text-slate-400"
        @keydown="handleKeydown"
      ></textarea>
      
      <button 
        class="flex-shrink-0 p-1.5 rounded-xl transition-colors"
        :class="[
          text.trim() ? 'bg-blue-600 text-white hover:bg-blue-700' : 'text-slate-400'
        ]"
        :disabled="!text.trim() || disabled"
        @click="send"
      >
        <SendHorizontal class="w-5 h-5" />
      </button>
    </div>
    <div v-if="disabled" class="mt-2 text-center">
      <p class="text-[10px] text-red-500 font-medium uppercase tracking-wider">
        Сеанс заблокирован или ожидается ответ
      </p>
    </div>
  </div>
</template>
