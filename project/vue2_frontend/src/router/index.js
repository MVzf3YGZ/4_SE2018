import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import regist from '@/components/regist.vue'
import echart1 from '@/components/echart1.vue'
import echart2 from '@/components/echart2.vue'
import echart3 from '@/components/echart3.vue'
import echart4 from '@/components/echart4.vue'
import choose from  '@/components/choose.vue'
import savepdf from  '@/components/savepdf.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/regist',
      name: 'regist',
      component: regist
    },
    {
      path: '/echart1',
      name: 'echart1',
      component: echart1
    },
    {
      path: '/echart2',
      name: 'echart2',
      component: echart2
    },
    {
      path: '/echart3',
      name: 'echart3',
      component: echart3
    },
    {
      path: '/echart4',
      name: 'echart4',
      component: echart4
    },
     {
      path: '/choose',
      name: 'choose',
      component: choose
    },
    {
      path: '/savepdf',
      name: 'savepdf',
      component: savepdf
    },
  ]
})
// router.beforeEach((to, from, next) => {
//   let token = window.localStorage.getItem('token') 
//   if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
//     next({
//       path: '/login',
//       query: { redirect: to.fullPath }
//     })
//   } else {
//     next()
//   }
// })