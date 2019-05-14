import { MESSAGES, PUSH_MESSAGE, OPEN_CHAT, CLOSE_CHAT, INC_COUNTER, RESET_COUNTER, MESS_NOTIFICATION, EVENT_NOTIFICATION } from 'store/mutations/chat'
import { MESSAGETOSERVER, ONE_MESSAGE, SET_CHAT_DIALOG, GET_MORE_MESSAGES } from 'store/actions/chat'
import Vue from 'vue'

export default {
  namespaced: true,
  state: {
    messages: [],
    count: 0,
    users: [],
    isDialogShow: false,
  },

  mutations: {
    [MESSAGES]: (state, payload) => {
      state.messages = [...payload['messages'].slice().reverse(), ...state.messages]
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
    },
    ['SOCKET_CHAT_USERSLIST']: (state, payload) => {
      state.users = payload
    },
    ['USER_IN']: (state, payload) => {
      Vue.set(state.users, payload['sid'], { username: payload['user'] })
    },
    ['USER_OUT']: (state, payload) => {
      Vue.delete(state.users, payload['sid'])
    }
  },

  actions: {
    ['socket_chatUserin']: ({ commit }, payload) => {
      console.log('userin', payload)
      commit('USER_IN', payload)
      payload.state = 'on'
      payload.place = 'online'
      commit(EVENT_NOTIFICATION, payload)
    },
    ['socket_chatUserout']: ({ commit }, payload) => {
      commit('USER_OUT', payload)
      payload.state = 'off'
      payload.place = 'offline'
      commit(EVENT_NOTIFICATION, payload)
    },

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
    [GET_MORE_MESSAGES]: ({ state }) => {
      (new Vue()).$socket.emit(GET_MORE_MESSAGES, state.messages[0].time)
    }
  }
}
