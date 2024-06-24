const CryptoJs = require('crypto-js')
//关键词是AES，mode，padding
let password = "tian";
let key = "1234567890abcdef"
// AES加密
cfg = {
  mode: CryptoJs.mode.ECB,
  padding: CryptoJs.pad.Pkcs7
}
let encPwd = CryptoJs.AES.encrypt(password, key, cfg).toString()
console.log(encPwd)

// AES解密
cfg = {
  mode: CryptoJs.mode.ECB,
  padding: CryptoJs.pad.Pkcs7
}
decPwd = CryptoJs.AES.decrypt(encPwd, key, cfg).toString(CryptoJs.enc.Utf8) // 指定解码方式
console.log(decPwd)