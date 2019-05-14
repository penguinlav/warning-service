import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vuetify/dist/vuetify.min.css'


import 'es6-promise/auto'
import 'babel-polyfill'
import Vue from 'vue'
import App from './App'
import router from './router'
import VueSocketio from 'vue-socket.io-extended'
import io from 'socket.io-client'
import Vuetify from 'vuetify'
import Notifications from 'vue-notification'
import store from './store/index'
import VueScrollTo from 'vue-scrollto'
import VueCookies from 'vue-cookies'
import VueMoment from 'vue-moment'

Vue.use(Notifications)
Vue.use(VueScrollTo)
Vue.use(VueCookies)
Vue.use(VueMoment)
Vue.use(Vuetify)
Vue.use(VueSocketio, io('http://' + location.host + '/ws', {autoConnect: false}), { store })

Vue.filter('reverse', function(value) {
  // slice to make a copy of array, then reverse the copy
  return value.slice().reverse();
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
