//距离
var c = [{
  left: Math.floor((i.left - y.operation.offset().left) / T.rate),
  top: Math.floor(parseInt(T.spt, 10))
}];

function encode() {
  for (var t = [], n = 0; n < e.length; n++)
    e[n] && (t[Math.floor(n / 6)] ^= 1 << n % 6);
  for (n = 0; n < t.length; n++)
    t[n] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".charAt(t[n] || 0);
  return t.join("")
}