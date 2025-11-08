import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../../pages/MainPage/MainPage.vue'
import LoginPage from '../../pages/LoginPage/LoginPage.vue'
import RegistePage from '../../pages/RegistePage/RegistePage.vue'

const routes = [
  {
    path: '/dashboard/',
    name: 'MainPage',
    component: MainPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/signin/',
    name: 'LoginPage',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/signup/',
    name: 'RegistePage',
    component: RegistePage,
    meta: { requiresGuest: true }
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const existingPage = to.matched.length > 0;
  const isAuthenticated = true;

 
  if (requiresAuth && !isAuthenticated) {
    next('/signin/')
  } else if (existingPage) {
      next()
    } else next('/dashboard/')
})

