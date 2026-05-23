<template>
  <div class="flex items-center space-x-1 px-4 py-2 bg-slate-100 rounded-2xl w-max">
    <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
    <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
    <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
.animate-bounce {
  animation: bounce 0.6s infinite ease-in-out;
}
</style>
