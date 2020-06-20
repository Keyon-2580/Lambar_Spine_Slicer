import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './config/router'
import Mint from 'mint-ui';
import 'mint-ui/lib/style.css';
import imagvue from 'imagvue'
Vue.use(imagvue)
Vue.use(Mint);
Vue.use(VueAxios, axios)
Vue.use(ElementUI)

Vue.prototype.$axios = axios
// Vue.prototype.$toast = Toast
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),

}).$mount('#app')

axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.timeout = 1000000