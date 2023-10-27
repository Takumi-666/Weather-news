import Vue from 'vue'
import App from './App.vue'
import router from './router'

// BootstrapのCSSをインポート
import 'bootstrap/dist/css/bootstrap.css'
// Bootstrap-Vueをインポート
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue } from 'bootstrap-vue'

// Vue Axiosをインポート
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: router,  
}).$mount('#app')
