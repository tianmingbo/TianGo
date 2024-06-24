const CryptoJs = require('crypto-js')
let key = 'salt';
let text = '123';
let hash = CryptoJs.HmacSHA256(text,key);
let hashInHex=CryptoJs.enc.Hex.stringify(hash);
console.log(hashInHex);