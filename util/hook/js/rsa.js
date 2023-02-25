window = global;
const JSEncrypt = require("node-jsencrypt");
const fs = require("fs");

window.JSEncrypt = JSEncrypt;
var data = "dali";
// var publickey = fs.readFileSync("./public.pem", 'utf8');
// var privatekey = fs.readFileSync("./private.pem", 'utf8');

//HOOK
var b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var b64pad = "=";

function hex2b64(h) {
  var i;
  var c;
  var ret = "";
  for (i = 0; i + 3 <= h.length; i += 3) {
    c = parseInt(h.substring(i, i + 3), 16);
    ret += b64map.charAt(c >> 6) + b64map.charAt(c & 63);
  }
  if (i + 1 == h.length) {
    c = parseInt(h.substring(i, i + 1), 16);
    ret += b64map.charAt(c << 2);
  } else if (i + 2 == h.length) {
    c = parseInt(h.substring(i, i + 2), 16);
    ret += b64map.charAt(c >> 2) + b64map.charAt((c & 3) << 4);
  }
  while ((ret.length & 3) > 0) {
    ret += b64pad;
  }
  return ret;
};

function b64tohex(s) {
  var ret = "";
  var i;
  var k = 0; // b64 state, 0-3
  var slop = 0;
  for (i = 0; i < s.length; ++i) {
    if (s.charAt(i) == b64pad) {
      break;
    }
    var v = b64map.indexOf(s.charAt(i));
    if (v < 0) {
      continue;
    }
    if (k == 0) {
      ret += int2char(v >> 2);
      slop = v & 3;
      k = 1;
    } else if (k == 1) {
      ret += int2char((slop << 2) | (v >> 4));
      slop = v & 0xf;
      k = 2;
    } else if (k == 2) {
      ret += int2char(slop);
      ret += int2char(v >> 2);
      slop = v & 3;
      k = 3;
    } else {
      ret += int2char((slop << 2) | (v >> 4));
      ret += int2char(v & 0xf);
      k = 0;
    }
  }
  if (k == 1) {
    ret += int2char(slop << 2);
  }
  return ret;
};
var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";

function int2char(n) {
  return BI_RM.charAt(n);
}

var RSA = window.JSEncrypt.prototype; //保存原型链
if (RSA != undefined) {
  var _RSA_setpubkey = RSA.setPublicKey;
  window.JSEncrypt.prototype.setPublicKey = function (a) {
    console.log("设置的公钥：", a);
    return RSA.setKey(a);
  };

  var _RSA_setprikey = RSA.setPrivateKey;
  window.JSEncrypt.prototype.setPrivateKey = function (a) {
    console.log("设置的私钥：", a);
    return RSA.setKey(a);
  };

  var _RSA_encrypt = RSA.encrypt;
  window.JSEncrypt.prototype.encrypt = function (a) {
    console.log("进行加密的信息：", a);
    return hex2b64(RSA.getKey().encrypt(a));
  };

  var _RSA_decrypt = RSA.decrypt;
  window.JSEncrypt.prototype.decrypt = function (a) {
    console.log("进行解密的信息：", a);
    return RSA.getKey().decrypt(b64tohex(a));
  }
}
;


// var key = new JSEncrypt();
// //公钥加密
// var pubkey = key.setPublicKey(publickey);
// var encodeData = key.encrypt(data);
// console.log(encodeData);
// //私钥解密
// var prikey = key.setPrivateKey(privatekey);
// var decodeData = key.decrypt(encodeData);
// console.log(decodeData);