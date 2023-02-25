window = global;
const CryptoJs = require("crypto-js");
window.CryptoJs = CryptoJs;


//Hook
var AES_enc = window.CryptoJs.AES.encrypt;
window.CryptoJs.AES.encrypt = function (a, b, c) {
  console.log("要加密的文本：", a.toString(CryptoJs.enc.Utf8));
  console.log("key：", b.toString(CryptoJs.enc.Utf8));
  console.log("iv：", c.iv.toString(CryptoJs.enc.Utf8));
  return AES_enc(a, b, c);
};

var AES_dec = window.CryptoJs.AES.decrypt;
window.CryptoJs.AES.decrypt = function (a, b, c) {
  console.log("要加密的文本：", a.toString(CryptoJs.enc.Utf8));
  console.log("key：", b.toString(CryptoJs.enc.Utf8));
  console.log("iv：", c.iv.toString(CryptoJs.enc.Utf8));
  return AES_dec(a, b, c);
};


var data = "dali";

const key = CryptoJs.enc.Utf8.parse("1234123412ABCDEF");  //十六位十六进制数作为密钥
const iv = CryptoJs.enc.Utf8.parse('1234123412ABCDEF');   //十六位十六进制数作为密钥偏移量

//加密方法
var encdata = CryptoJs.enc.Utf8.parse(data);
var encrypted = CryptoJs.AES.encrypt(encdata, key, {iv: iv, mode: CryptoJs.mode.CBC, padding: CryptoJs.pad.Pkcs7});
console.log(encrypted.toString());

//解密方法
var encryptedHexStr = CryptoJs.enc.Hex.parse(encrypted.ciphertext.toString());
var decdata = CryptoJs.enc.Base64.stringify(encryptedHexStr);

var decrypt = CryptoJs.AES.decrypt(decdata, key, {iv: iv, mode: CryptoJs.mode.CBC, padding: CryptoJs.pad.Pkcs7});
var decryptedStr = decrypt.toString(CryptoJs.enc.Utf8);
console.log(decryptedStr);
