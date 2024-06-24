const CryptoJS = require("crypto-js");

//知识点：日志log输出，hook函数调用
/**
 * var old = _[1][0]['CryptoJS']['AES'].encrypt;

 _[1][0]['CryptoJS']['AES'].encrypt = function(a, b, c, d, e) {
    debugger;
    var bb = old(a, b, c,d,e);
    console.log(bb.toString())
    debugger;
    return bb;
    };
 *
 * */
function AESencrypt(data, key, iv) {
  var key1 = CryptoJS.enc.Utf8.parse(key);
  var iv1 = CryptoJS.enc.Utf8.parse(iv);
  return CryptoJS.AES.encrypt(data, key1, {
    iv: iv1,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  }).toString();
}

function getV(t, pageNum) {
  // t=1676890871
  // pageNum=2
  var key = iv = t.toString(16) + t.toString(16)
  data = pageNum.toString() + "|" + "300m323,300d323,300m323,300u323,393u20"
  res = AESencrypt(data, key, iv)
  return res;
}
// console.log(getV())
//
const t = parseInt(process.argv[2]);
let result;
const pageNum = parseInt(process.argv[3]);
result = getV(t, pageNum);
console.log(result)