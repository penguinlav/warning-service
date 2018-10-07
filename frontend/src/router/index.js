import Vue from 'vue'
import Router from 'vue-router'
// import Home from 'components/home'
// import Account from 'components/account'
import Login from 'components/login'
import AppNav from 'components/appnav'
import CoreFeature from 'components/corefeature'
import Chat from 'components/chat'
import store from '../store'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  console.log('ifNotAuthenticated')
  if (!store.getters['auth/isAuthenticated']) {
    console.log(store.getters['auth/isAuthenticated'])
    console.log(window.$cookies.get('AIOHTTP_SESSION'))
    console.log('next(): ' + !store.getters.isAuthenticated)

    next()
    return
  }
  console.log('next("/")')

  next('/')
}

const ifAuthenticated = (to, from, next) => {
  console.log('ifAuthenticated')

  if (store.getters['auth/isAuthenticated']) {
    next()
    return
  }
  next('/login')
}

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      components: {
        default: AppNav,
      },
      children: [
        {
          path: '/chat',
          name: 'Chat',
          components: {
            // default: AppNav,
            workspace: Chat

          },
        },
        {
          path: '/home',
          name: 'Home',
          components: {
            // default: AppNav,
            workspace: CoreFeature
          },
          beforeEnter: ifAuthenticated,
        },
      ],
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/chat',
      name: 'Chat',
      components: {
        default: AppNav,
        workspace: Chat

      },
      beforeEnter: ifAuthenticated,
    },

  ],
})