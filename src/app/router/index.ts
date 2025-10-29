import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../../pages/MainPage/MainPage.vue'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})