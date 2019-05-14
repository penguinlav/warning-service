import axios from 'axios'
import router from 'router'

const mocks = {
  'auth': { 'POST': { token: 'This-is-a-mocked-token' } },
  'user/me': { 'GET': { name: 'doggo', title: 'sir' } }
}

const apiCall = function ({ url, method, data, ...args }) {
  console.log(method)
  console.log(args)
  return axios({ url: 'api/' + url, data: data, method: method, withCredentials: true }).catch(err => {
    if (err.response.status == 401) {
      router.push('/login')
    }
    return Promise.reject(err)
  })
}

export default apiCall