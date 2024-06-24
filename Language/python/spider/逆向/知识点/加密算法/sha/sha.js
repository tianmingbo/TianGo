const CryptoJs = require('crypto-js')
//sha1加密的关键词是 Sha1
let pwd = '123';
let encode = CryptoJs.SHA1(pwd).toString();
console.log(encode);