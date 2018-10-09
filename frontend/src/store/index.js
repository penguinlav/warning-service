
import Vuex from 'vuex'
import Vue from 'vue'

import core_features from './modules/core_features'
import auth from './modules/auth'
import chat from 'store/modules/chat'
import { START_WEBSOCKET, STOP_WEBSOCKET, START_UP_TIME, ERROR_NOTIFICATION } from 'store/actions/default'
import { INTERRUPT_SESSION } from 'store/actions/auth'

import router from 'router'
import VueCookies from 'vue-cookies'
import { GET_PROFILE } from './actions/auth';

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    core_features,
    auth,
    chat
  },

  state: {
    isConnected: false,
    now: + new Date,
  },

  mutations: {
    SOCKET_CONNECT(state, status) {
      console.log('ws connect')
      state.isConnected = true;
    },
    SOCKET_DISCONNECT(state, status) {
      console.log('ws disconnect', status)
      state.isConnected = false;
    },
    UPDATE_TIME(state) {
      state.now = + new Date
    },
  },

  actions: {
    socket_connectError({ state, commit, dispatch }, err) {
      commit('ERROR', "Error connect socket")
      dispatch(ERROR_NOTIFICATION, { title: "Error connect websocket", type: 'error', text: '' })
      dispatch('auth/' + GET_PROFILE).catch(err => { // чекаем валидность кукисов, простой дисконнект или перезагрузка сервера
        if (err.response.status == 401) {
          dispatch('auth/' + INTERRUPT_SESSION)
        }
      })
    },
    [START_UP_TIME]: ({ commit }) => {
      setInterval(() => {
        commit('UPDATE_TIME')
      }, 1000 * 20)
    },
    [START_WEBSOCKET]: ({ dispatch }) => {
      (new Vue).$socket.open()
    },
    [STOP_WEBSOCKET]: () => {
      (new Vue).$socket.close()
    },
    [ERROR_NOTIFICATION]: ({ }, { title, type, text }) => {
      Vue.notify({
        group: 'nav',
        title: title,
        text: text,
        type: type
      })
    }
  },
})