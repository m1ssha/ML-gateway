<script setup>
import { ShieldCheck, LayoutDashboard, MessageSquare } from 'lucide-vue-next'
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="flex flex-col h-screen overflow-hidden">
    <header class="bg-white border-b border-stone-200 px-6 py-4 flex items-center justify-between z-10">
      <div class="flex items-center space-x-3">
        <div class="bg-emerald-600 p-1.5 rounded-lg">
          <ShieldCheck class="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 class="font-bold text-stone-800 leading-tight tracking-tight">LLM Gateway</h1>
          <p class="text-[10px] text-stone-400 uppercase font-semibold tracking-widest">Защищённый шлюз доступа</p>
        </div>
      </div>

      <nav class="flex items-center space-x-1 bg-stone-100 p-1 rounded-xl">
        <RouterLink
          to="/"
          class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="route.path === '/' ? 'bg-white text-emerald-600 shadow-sm' : 'text-stone-500 hover:text-stone-800'"
        >
          <MessageSquare class="w-4 h-4" />
          <span>Чат</span>
        </RouterLink>
        <RouterLink
          to="/admin"
          class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="route.path === '/admin' ? 'bg-white text-emerald-600 shadow-sm' : 'text-stone-500 hover:text-stone-800'"
        >
          <LayoutDashboard class="w-4 h-4" />
          <span>Админ</span>
        </RouterLink>
      </nav>
    </header>

    <main class="flex-1 relative bg-stone-50 overflow-hidden">
      <RouterView v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<style>
.page-enter-active {
  transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.page-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
