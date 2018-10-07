import Vue from 'vue'
var audio = new Audio(require('./../../assets/beep-03.mp3'))
export default {
  namespaced: true,

  state: {
    states: false,
  },

  mutations: {
    SOCKET_CORE_UPDSTATES(state, payload) {
      console.log('socket: switch state cp: ' + payload)
      state.states = payload
      console.log('mut upd')
      
    },
    // SOCKET_CONNECT(state) {
    //   console.log('ws connect dispatch')
    // },
  },

  actions: {
    updState({ state }, payload) {
      console.log('switch state: '+ payload);
      (new Vue()).$socket.emit('core_updstate', payload)
      // this.$socket.emit('switch_state', {1:1})
    },
    socket_CORE_UPDSTATES({commit}, payload) {
      console.log('action upd')
    }
  },
  

  getters: {
    connectState: (state) => state.isConnected
  }
}