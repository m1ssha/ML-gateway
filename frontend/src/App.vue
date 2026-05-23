<script setup>
import { ShieldCheck, LayoutDashboard, MessageSquare } from 'lucide-vue-next'
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="app-layout">
    <aside class="app-sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <ShieldCheck class="brand-icon" />
          <div class="brand-text">
            <span class="brand-title">ML Gateway</span>
            <span class="brand-subtitle">Secure access</span>
          </div>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <RouterLink 
          to="/" 
          class="nav-item" 
          :class="{ active: route.path === '/' }"
        >
          <MessageSquare class="nav-icon" />
          <span>Chat</span>
        </RouterLink>
        <RouterLink 
          to="/admin" 
          class="nav-item" 
          :class="{ active: route.path === '/admin' }"
        >
          <LayoutDashboard class="nav-icon" />
          <span>Admin</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="version-tag">v1.2.0</div>
      </div>
    </aside>

    <main class="app-main">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  background-color: var(--color-white);
}

.app-sidebar {
  width: 260px;
  background-color: var(--color-gray-900);
  color: var(--color-white);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: var(--space-6) var(--space-4);
}

.brand {
  display: flex;
  items-center: center;
  gap: var(--space-3);
}

.brand-icon {
  width: 28px;
  height: 28px;
  color: var(--color-primary);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: -0.01em;
}

.brand-subtitle {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-gray-500);
  font-weight: 600;
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-3);
  border-radius: var(--border-radius-md);
  color: var(--color-gray-400);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: var(--color-gray-800);
  color: var(--color-white);
}

.nav-item.active {
  background-color: var(--color-gray-800);
  color: var(--color-white);
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--color-gray-800);
}

.version-tag {
  font-size: 0.7rem;
  color: var(--color-gray-600);
  font-family: var(--font-mono);
}

.app-main {
  flex: 1;
  overflow: hidden;
  position: relative;
  background-color: var(--color-white);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
