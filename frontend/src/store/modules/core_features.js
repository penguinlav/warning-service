import Vue from 'vue'
var audio = new Audio(require('./../../assets/beep-03.mp3'))
import { ONE_MESSAGE } from 'store/actions/chat'
export default {
  namespaced: true,

  state: {
    states: {},
  },

  getters: {
    isAFK: state => state.states['afk'],
    connectState: (state) => state.isConnected
  },

  mutations: {
    SOCKET_CORE_UPDSTATES(state, payload) {
      console.log('socket: switch state cp: ', payload)
      state.states = payload
      console.log('mut upd')
    },
  },

  actions: {
    updState({ state }, payload) {
      console.log('switch state: ', payload);
      (new Vue()).$socket.emit('core_updstate', payload)
    },
    socket_CORE_UPDSTATES({ commit }, payload) {
      console.log('action upd ', payload)
    },
    socket_coreEvent({ dispatch }, payload) {
      payload['type'] = 'event'
      dispatch('chat/' + ONE_MESSAGE, payload, { root: true })
      console.log('event ', payload)
    }
  },
}