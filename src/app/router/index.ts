import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../../pages/MainPage/MainPage.vue'
import LoginPage from '../../pages/LoginPage/LoginPage.vue'
import RegistePage from '../../pages/RegistePage/RegistePage.vue'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/signup',
    name: 'RegistePage',
    component: RegistePage,
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})