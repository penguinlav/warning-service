// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vuetify/dist/vuetify.min.css'


import Vue from 'vue'
import App from './App'
import router from './router'
import VueSocketio from 'vue-socket.io-extended'
import io from 'socket.io-client'
import Vuetify from 'vuetify'
import Notifications from 'vue-notification'
Vue.use(Notifications)

var VueScrollTo = require('vue-scrollto');
 
Vue.use(VueScrollTo)

import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
Vue.use(require('vue-moment'))

Vue.filter('reverse', function(value) {
  // slice to make a copy of array, then reverse the copy
  return value.slice().reverse();
});

// const PORT = 8000
// const PORT_WS = process.env.PORT_WS
console.log(process.env)

Vue.use(Vuetify, {
  // theme: {
  //   primary: "#f44336",
  //   secondary: "#FFEBEE",
  //   accent: "#9c27b0",
  //   error: "#f44336",
  //   warning: "#ffeb3b",
  //   info: "#2196f3",
  //   success: "#4caf50"
  // }
})

import store from './store/index'


Vue.use(VueSocketio, io('http://' + location.host + '/ws', {autoConnect: false}), { store })

Vue.config.productionTip = true
Vue.config.devtools = true //true

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
