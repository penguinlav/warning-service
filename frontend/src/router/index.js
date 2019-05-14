import Vue from 'vue'
import Router from 'vue-router'
import Login from 'components/login'
import AppNav from 'components/appnav'
import CoreFeature from 'components/corefeature'
import Chat from 'components/chat'
import Changelog from 'components/changelog'
import store from '../store'
import Localhost from 'components/localhost'

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
      redirect: '/home',
      components: {
        default: AppNav,
      },
      children: [
        {
          path: '/chat',
          name: 'Chat',
          components: {
            workspace: Chat

          },
        },
        {
          path: '/home',
          name: 'Home',
          components: {
            workspace: CoreFeature
          },
          beforeEnter: ifAuthenticated,
        },
        {
          path: '/changelog',
          name: 'Changelog',
          components: {
            workspace: Changelog
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
      path: '/localhost-deny',
      name: 'localhost-deny',
      component: Localhost,
    },
  ],
})