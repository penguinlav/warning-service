
import Vuex from 'vuex'
import Vue from 'vue'

import core_features from './modules/core_features'
import auth from './modules/auth'
import chat from 'store/modules/chat'
import { START_WEBSOCKET, STOP_WEBSOCKET, START_UP_TIME } from './actions/default'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    core_features,
    auth,
    chat
  },

  state: {
    isConnected: false,
    now: + new Date
  },

  mutations: {
    SOCKET_CONNECT(state, status) {
      console.log('ws connect')
      state.isConnected = true;
    },
    SOCKET_DISCONNECT(state, status) {
      console.log('ws disconnect')
      state.isConnected = false;
    },
    UPDATE_TIME (state) {
      state.now = + new Date
    }
  },

  actions: {
    [START_UP_TIME]: ({ commit }) => {
      setInterval(() => {
        commit('UPDATE_TIME')
      }, 1000 * 20)
    },

    [START_WEBSOCKET]: () => {
      // console.log('start START_WEBSOCKET')
      (new Vue).$socket.open()
    },
    [STOP_WEBSOCKET]: () => {
      (new Vue).$socket.close()
    },
  },
})