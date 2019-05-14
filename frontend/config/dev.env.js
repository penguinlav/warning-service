'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
// console.log('++++=========ENV: ' + JSON.stringify(prodEnv))

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  PORT_WS: 8000
})
