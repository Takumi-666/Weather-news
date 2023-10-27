//index.js

import Vue from 'vue';
import VueRouter from 'vue-router';
import MyHome from '@/components/MyHome.vue';
import AppWeather from '@/components/AppWeather.vue'; // AppWeather.vue のパスを適切に設定

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'MyHome',
    component: MyHome, 
  },
  {
    path: '/appWeather',
    name: 'AppWeather',
    component: AppWeather,
  },
];

const router = new VueRouter({
  routes,
});

export default router;