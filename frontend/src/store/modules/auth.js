import axios from 'axios'
import Vue from 'vue'

import { AUTH_REQUEST, AUTH_ERROR, AUTH_SUCCESS, AUTH_LOGOUT, UPDATE_TOKEN } from 'store/actions/auth'
import { STOP_WEBSOCKET } from 'store/actions/default'

import apiCall from '../utils/api'

import VueCookies from 'vue-cookies'


export default {
  namespaced: true,

  state: {
    token: window.$cookies.get('AIOHTTP_SESSION') || '',  //localStorage.getItem('user-token') || '',
    status: '',
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
            console.log('auth succsess')
            // localStorage.setItem('user-token', resp.token)
            // Here set the header of your ajax library to the token value.
            // example with axios
            // axios.defaults.headers.common['Authorization'] = resp.token
            commit(AUTH_SUCCESS)
            commit(UPDATE_TOKEN)

            // dispatch(USER_REQUEST)
            resolve(resp)
          })
          .catch(err => {
            console.log('auth error')

            console.log("Api error: ", err)
            commit(AUTH_ERROR, err)
            // localStorage.removeItem('user-token')
            reject(err)
          })
      })
    },
    [AUTH_LOGOUT]: ({ commit, dispatch, getters }) => {
      return new Promise((resolve, reject) => {
        // commit(AUTH_LOGOUT)
        // localStorage.removeItem('user-token')
        console.log('AUTH_LOGOUT 2')


        apiCall({ url: 'signout', method: 'GET' })
          .then(resp => {
            // localStorage.setItem('user-token', resp.token)
            // Here set the header of your ajax library to the token value.
            // example with axios
            // axios.defaults.headers.common['Authorization'] = resp.token
            // commit(AUTH_SUCCESS, resp)
            // dispatch(USER_REQUEST)
            // resolve(resp)
            console.log('then signout api')


          })
          .catch(err => {
            // commit(AUTH_ERROR, err)
            // localStorage.removeItem('user-token')
            // reject(err)
          }).finally(() => {
            commit(UPDATE_TOKEN)
            if (!getters.isAuthenticated) {
              dispatch(STOP_WEBSOCKET, null, { root: true })
            }
            resolve()
          })
      })
    },
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
    }
  }
}