import { createRouter, createWebHistory } from 'vue-router'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      component: ChatWindow
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/components/admin/AdminDashboard.vue')
    }
  ]
})

export default router
