import axios from 'axios'
import Vue from 'vue'
import VueCookies from 'vue-cookies'
import { AUTH_REQUEST, AUTH_ERROR, AUTH_SUCCESS, AUTH_LOGOUT, UPDATE_TOKEN, GET_PROFILE, INTERRUPT_SESSION, FORCE_LOGOUT } from 'store/actions/auth'
import { UPDATE_PROFILE, REMOVE_COOKIE } from 'store/mutations/auth'
import { STOP_WEBSOCKET } from 'store/actions/default'
import apiCall from '../utils/api'
import router from 'router'

export default {
  namespaced: true,
  state: {
    token: window.$cookies.get('AIOHTTP_SESSION') || '',
    status: '',
    profile: { username: '' }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
  },
  actions: {
    [AUTH_REQUEST]: ({ commit, dispatch }, user) => {
      return new Promise((resolve, reject) => {
        commit(AUTH_REQUEST)
        apiCall({ url: 'auth', data: user, method: 'POST', })
          .then(resp => {
            commit(AUTH_SUCCESS)
            commit(UPDATE_TOKEN)
            dispatch(GET_PROFILE)
            resolve(resp)
          })
          .catch(err => {
            console.log('auth error')
            console.log("Api error: ", err)
            commit(AUTH_ERROR, err)
            reject(err)
          })
      })
    },
    [AUTH_LOGOUT]: ({ commit, dispatch, getters }) => {
      return new Promise((resolve, reject) => {
        apiCall({ url: 'signout', method: 'GET' })
          .then(resp => {
          })
          .finally(() => {
            dispatch(REMOVE_COOKIE)
            if (!getters.isAuthenticated) {
              dispatch(STOP_WEBSOCKET, null, { root: true })
            }
            router.push('/login')
            resolve()
          })
      })
    },
    [GET_PROFILE]: ({ commit }) => {
      return new Promise((resolve, reject) => {
        apiCall({ url: 'profile', method: 'GET' })
          .then(resp => {
            commit(UPDATE_PROFILE, resp.data)
            resolve(resp)
          })
          .catch(err => {
            console.log('Profile error: ', err)
            reject(err)
          })
      })

    },
    [REMOVE_COOKIE]: ({ commit }) => {
      (new Vue).$cookies.remove('AIOHTTP_SESSION')
      commit(UPDATE_TOKEN)
    },
    [INTERRUPT_SESSION]: ({ dispatch, commit }) => {
      dispatch(STOP_WEBSOCKET, null, { root: true })
      dispatch(REMOVE_COOKIE)
      router.push('/login')
    },
    [FORCE_LOGOUT]: ({ dispatch }) => {
      console.log('You are kicked')
      dispatch(AUTH_LOGOUT)
    }
  },
  mutations: {
    [AUTH_REQUEST]: (state) => {
      state.status = 'loading'
    },
    [AUTH_SUCCESS]: (state) => {
      state.status = 'success'
    },
    [AUTH_ERROR]: (state) => {
      state.status = 'error'
    },
    [AUTH_LOGOUT]: (state, token) => {
    },
    [UPDATE_TOKEN]: (state) => {
      state.token = window.$cookies.get('AIOHTTP_SESSION') || ''
      console.log('token updated')
    },
    [UPDATE_PROFILE]: (state, payload) => {
      console.log('Profile: ', payload)
      state.profile = payload
    }
  }
}