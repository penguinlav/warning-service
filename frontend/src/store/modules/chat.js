import { MESSAGES, PUSH_MESSAGE, OPEN_CHAT, CLOSE_CHAT, INC_COUNTER, RESET_COUNTER, MESS_NOTIFICATION, EVENT_NOTIFICATION } from 'store/mutations/chat'
import { MESSAGETOSERVER, ONE_MESSAGE, SET_CHAT_DIALOG } from 'store/actions/chat'
import Vue from 'vue'

export default {
  namespaced: true,
  state: {
    messages: [],
    count: 0,
    isDialogShow: false,
  },

  mutations: {
    [MESSAGES]: (state, payload) => {
      state.messages = payload['messages'].slice().reverse()
      state.isNewMess = true
    },
    [PUSH_MESSAGE]: (state, payload) => {
      state.messages.push(payload)
    },
    [OPEN_CHAT]: (state) => {
      state.isDialogShow = true
    },
    [CLOSE_CHAT]: (state) => {
      state.isDialogShow = false
    },
    [INC_COUNTER]: (state) => {
      state.count++
    },
    [RESET_COUNTER]: (state) => {
      state.count = 0
    },
    [MESS_NOTIFICATION]: (state, payload) => {
      console.log('MESS ', payload)

      Vue.notify({
        group: 'chat',
        title: payload.user,
        text: payload.msg
      })
    },
    [EVENT_NOTIFICATION]: (state, payload) => {
      console.log('EEVEEENTTT ', payload)
      Vue.notify({
        group: 'event',
        title: payload.user,
        text: payload.place + ' ' + payload.state,
        type: payload.state == 'on' ? 'error' : 'success'
      })
    }
  },

  actions: {
    [SET_CHAT_DIALOG]: ({ commit, state }, payload) => {
      if (payload && !state.isDialogShow) {
        commit(OPEN_CHAT)
        if (state.count) {
          commit(RESET_COUNTER)
        }
      }
      if (!payload && state.isDialogShow) {
        commit(CLOSE_CHAT)
      }
    },
    [ONE_MESSAGE]: ({ commit, state, dispatch, rootState }, payload) => {
      commit(PUSH_MESSAGE, payload)
      if (!state.isDialogShow) {
        if (payload.user != rootState.auth.profile.username) {
          commit(INC_COUNTER)
          if (payload.type == 'event') {
            commit(EVENT_NOTIFICATION, payload)
          } else {
            commit(MESS_NOTIFICATION, payload)
          }
        }

      }
    },
    [MESSAGETOSERVER]: ({ state }, payload) => {
      (new Vue()).$socket.emit(MESSAGETOSERVER, payload)
    },

  }
}