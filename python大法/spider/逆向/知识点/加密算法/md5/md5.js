const CryptoJs = require('crypto-js')

let pwd = '123';
let encode = CryptoJs.MD5(pwd).toString();
console.log(encode);