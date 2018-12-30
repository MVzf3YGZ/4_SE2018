// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import './element'
import echarts from 'echarts'
import axios from 'axios'
import VueResource from 'vue-resource'
import html2canvas from 'html2canvas'
import store from './vuex'

require('echarts');
require('echarts-wordcloud');
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false
Vue.use(VueResource)
Vue.prototype.$ajax = axios;
Vue.prototype.$html2canvas = html2canvas;
// Vue.prototype.$store = store;


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
