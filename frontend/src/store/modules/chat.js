import { MESSAGES, PUSH_MESSAGE, OPEN_CHAT, CLOSE_CHAT, INC_COUNTER, RESET_COUNTER } from 'store/mutations/chat'
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
      console.log('receive from socket messages: ' + payload)
      state.messages = payload['messages']
      state.isNewMess = true
    },
    [PUSH_MESSAGE]: (state, payload) => {
      console.log('receive from socket message: ' + payload)
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
    }
  },

  actions: {
    [SET_CHAT_DIALOG]: ({commit, state}, payload) => {
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
    [ONE_MESSAGE]: ({commit, state}, payload) => {
      commit(PUSH_MESSAGE, payload)
      if (!state.isDialogShow) {
        commit(INC_COUNTER)
      }
    },
    [MESSAGETOSERVER]: ({state}, payload) => {
      // console.log('Send to server: ' + payload)
      (new Vue()).$socket.emit(MESSAGETOSERVER, payload)
    }
  }
}