import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/recommend' },
  { path: '/recommend', name: 'Recommend', component: () => import('../views/RecommendView.vue') },
  { path: '/record', name: 'Record', component: () => import('../views/RecordView.vue') },
  { path: '/history', name: 'History', component: () => import('../views/HistoryView.vue') },
  { path: '/statistics', name: 'Statistics', component: () => import('../views/StatisticsView.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/ProfileView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
