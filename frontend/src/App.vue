<script setup>
import { ShieldCheck, LayoutDashboard, MessageSquare } from 'lucide-vue-next'
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="flex flex-col h-screen overflow-hidden">
    <!-- Navbar -->
    <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between z-10">
      <div class="flex items-center space-x-3">
        <div class="bg-blue-600 p-1.5 rounded-lg">
          <ShieldCheck class="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 class="font-bold text-slate-900 leading-tight">LLM Gateway</h1>
          <p class="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Защищённый шлюз доступа</p>
        </div>
      </div>

      <nav class="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl">
        <RouterLink 
          to="/" 
          class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="route.path === '/' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
        >
          <MessageSquare class="w-4 h-4" />
          <span>Чат</span>
        </RouterLink>
        <RouterLink 
          to="/admin" 
          class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="route.path === '/admin' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'"
        >
          <LayoutDashboard class="w-4 h-4" />
          <span>Админ</span>
        </RouterLink>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="flex-1 relative bg-slate-50 overflow-hidden">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
