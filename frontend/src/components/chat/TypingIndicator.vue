<template>
  <div class="typing-indicator">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>
</template>

<style scoped>
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: var(--space-2) var(--space-4);
  background-color: var(--color-gray-50);
  border-radius: var(--border-radius-md);
  width: fit-content;
}

.dot {
  width: 6px;
  height: 6px;
  background-color: var(--color-gray-300);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>
