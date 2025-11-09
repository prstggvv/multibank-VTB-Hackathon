import { createApp } from 'vue'
import './app/styles/style.css'
import App from './app/App.vue'
import { router } from './app/router';
import { createPinia } from 'pinia';

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);
app.use(router)
app.mount('#app')
