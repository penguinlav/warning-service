export function toColor(str) {
  var hash = 0
  var len = str.length
  if (len === 0) return 'black'
  for (var i = 0; i < len; i++) {
    hash = ((hash << 8) - hash) + str.charCodeAt(i)
    hash |= 0
  }
  hash = Math.abs(hash)
  return '#' + hash.toString(16).substr(0, 6)
}