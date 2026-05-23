<script setup>
import { ref, onMounted, watch } from 'vue'
import { Send } from 'lucide-vue-next'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send'])
const message = ref('')
const textareaRef = ref(null)

const adjustHeight = () => {
  if (!textareaRef.value) return
  textareaRef.value.style.height = 'auto'
  textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`
}

watch(message, () => {
  setTimeout(adjustHeight, 0)
})

const handleSend = () => {
  if (message.value.trim() && !props.disabled) {
    emit('send', message.value)
    message.value = ''
    setTimeout(adjustHeight, 0)
  }
}
</script>

<template>
  <div class="input-area" :class="{ 'is-disabled': disabled }">
    <div class="input-container">
      <textarea
        ref="textareaRef"
        v-model="message"
        rows="1"
        placeholder="Send a message..."
        class="input-textarea"
        :disabled="disabled"
        @keydown.enter.prevent="handleSend"
        @input="adjustHeight"
      ></textarea>
      
      <button
        @click="handleSend"
        :disabled="disabled || !message.trim()"
        class="send-button"
      >
        <Send class="send-icon" />
      </button>
    </div>
    <div class="input-hint">
      Press Enter to send, Shift + Enter for new line
    </div>
  </div>
</template>

<style scoped>
.input-area {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-container {
  position: relative;
  display: flex;
  align-items: flex-end;
  background-color: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--border-radius-lg);
  padding: var(--space-2) var(--space-3);
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.input-container:focus-within {
  border-color: var(--color-gray-400);
  box-shadow: var(--shadow-md);
}

.is-disabled .input-container {
  background-color: var(--color-gray-50);
  cursor: not-allowed;
}

.input-textarea {
  flex: 1;
  border: none;
  background: transparent;
  padding: var(--space-2) var(--space-2);
  font-size: 1rem;
  line-height: 1.5;
  color: var(--color-gray-800);
  resize: none;
  max-height: 200px;
  min-height: 44px;
}

.input-textarea:focus {
  outline: none;
}

.input-textarea::placeholder {
  color: var(--color-gray-400);
}

.send-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  margin-bottom: var(--space-1);
  transition: all 0.2s ease;
}

.send-button:disabled {
  background-color: var(--color-gray-200);
  color: var(--color-gray-400);
  cursor: not-allowed;
}

.send-button:not(:disabled):hover {
  background-color: var(--color-primary-hover);
}

.send-icon {
  width: 16px;
  height: 16px;
}

.input-hint {
  font-size: 0.7rem;
  color: var(--color-gray-400);
  text-align: center;
  font-weight: 500;
}
</style>
