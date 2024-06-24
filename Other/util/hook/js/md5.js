const CryptoJs = require("crypto-js");

//模拟登录  document end  button登录  end
var _MD5 = window.CryptoJs.MD5;
window.CryptoJs.MD5 = function (data) {
  console.log("MD5 加密信息：", data);
  return _MD5(data);
};


var data = "dali";
console.log(CryptoJs.MD5(data).toString());