<script setup>
import { ShieldCheck, LayoutDashboard, MessageSquare } from 'lucide-vue-next'
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="flex flex-col h-screen overflow-hidden font-sans">
    <!-- Floating Header -->
    <header class="fixed top-6 left-1/2 -translate-x-1/2 w-[calc(100%-3rem)] max-w-5xl z-50">
      <div class="glass-panel px-6 py-3 rounded-2xl flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="bg-indigo-600/10 p-2 rounded-xl border border-indigo-600/20">
            <ShieldCheck class="w-6 h-6 text-indigo-600" />
          </div>
          <div>
            <h1 class="font-bold text-slate-800 leading-tight tracking-tight">LLM Gateway</h1>
            <p class="text-[10px] text-slate-400 uppercase font-bold tracking-[0.2em]">Secure Access</p>
          </div>
        </div>

        <nav class="flex items-center space-x-1 bg-slate-100/50 p-1 rounded-xl border border-white/40">
          <RouterLink
            to="/"
            class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300"
            :class="route.path === '/' ? 'bg-white text-indigo-600 shadow-sm border border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
          >
            <MessageSquare class="w-4 h-4" />
            <span>Chat</span>
          </RouterLink>
          <RouterLink
            to="/admin"
            class="flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300"
            :class="route.path === '/admin' ? 'bg-white text-indigo-600 shadow-sm border border-slate-200/50' : 'text-slate-500 hover:text-slate-800'"
          >
            <LayoutDashboard class="w-4 h-4" />
            <span>Admin</span>
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="flex-1 relative overflow-hidden pt-28 pb-8 px-6">
      <div class="h-full max-w-5xl mx-auto">
        <RouterView v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </main>
  </div>
</template>

<style>
.page-enter-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.99);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.99);
}
</style>
