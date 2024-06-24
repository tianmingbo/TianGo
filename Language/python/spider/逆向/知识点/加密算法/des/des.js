const CryptoJs = require('crypto-js')
//搜索关键字是DES、mode、padding
let pwd = CryptoJs.enc.Utf8.parse('123456');
let key = CryptoJs.enc.Utf8.parse('1234567');
cfg = {
  mode: CryptoJs.mode.ECB,
  padding: CryptoJs.pad.Pkcs7
}
//加密
let encPwd = CryptoJs.DES.encrypt(pwd, key, cfg).toString();
//解密
let decPwd = CryptoJs.DES.decrypt(encPwd, key, cfg).toString(CryptoJs.enc.Utf8);

console.log(encPwd, decPwd);