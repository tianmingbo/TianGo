const CryptoJs = require("crypto-js");

var _sha1 = CryptoJs.SHA1;
CryptoJs.SHA1 = function (data) {
  if (data != null) {
    console.log("SHA1 明文数据：", data);
    console.log("SHA1 密文数据：", String(_sha1(data)));
    return _sha1(data)
  }
};
var _sha256 = CryptoJs.SHA256;
CryptoJs.SHA256 = function (data) {
  if (data != null) {
    console.log("SHA256 明文数据：", data);
    console.log("SHA256 密文数据：", String(_sha256(data)));
    return _sha256(data)
  }
};


var data = "dali";
console.log(CryptoJs.SHA1(data).toString().length);
console.log(CryptoJs.SHA256(data).toString().length);