<template>
  <div class="flex items-center space-x-1.5 px-4 py-2 bg-stone-100 rounded-2xl max-w-max">
    <div class="w-1.5 h-1.5 bg-stone-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
    <div class="w-1.5 h-1.5 bg-stone-400 rounded-full animate-bounce" style="animation-delay: 120ms"></div>
    <div class="w-1.5 h-1.5 bg-stone-400 rounded-full animate-bounce" style="animation-delay: 240ms"></div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-5px) scale(0.85); }
}
.animate-bounce {
  animation: bounce 0.5s infinite cubic-bezier(0.32, 0, 0.67, 0);
}
</style>