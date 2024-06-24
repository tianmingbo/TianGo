CryptoJS = require("crypto-js")

!function (func) {
  function acvs() {
    var kk = func[1].call(null, 1e3);
    var data = {
      r: "I LOVE PYTHON",
      e: kk,
      i: "62bs819idl00oac2",
      k: "0123456789abcdef"
    }
    return func[0].call(data);
  }

  console.log("加密文本：" + acvs())

  function odsc(account) {
    var cr = false;
    var regExp = /(^\d{7,8}$)|(^0\d{10,12}$)/;
    if (regExp.test(account)) {
      cr = true;
    }
    return cr;
  }

  function mkle(account) {
    var cr = false;
    var regExp = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (regExp.test(account)) {
      cr = true;
    }
    return cr;
  }

}([
  function () {
    for (var n = "", t = 0; t < this.r.length; t++) {
      var o = this.e ^ this.r.charCodeAt(t);
      n += String.fromCharCode(o)
    }
    return encodeURIComponent(n)
  },
  function (x) {
    return Math.ceil(x * Math.random())
  },
  function (e) {
    var a = CryptoJS.MD5(this.k);
    var c = CryptoJS.enc.Utf8.parse(a);
    var d = CryptoJS.AES.encrypt(e, c, {
      iv: this.i
    });
    return d + ""
  },
  function (e) {
    var b = CryptoJS.MD5(this.k);
    var d = CryptoJS.enc.Utf8.parse(b);
    var a = CryptoJS.AES.decrypt(e, d, {
      iv: this.i
    }).toString(CryptoJS.enc.Utf8);
    return a
  }
]);

//以上用到了webpack模块化，可以改写如下：
function a(x) {
  return Math.ceil(x * Math.random())
}

function b(r, e) {
  for (var n = "", t = 0; t < r.length; t++) {
    var o = e ^ r.charCodeAt(t);
    n += String.fromCharCode(o)
  }
  return encodeURIComponent(n)
}

var kk = a(1e3);
var data = {
  r: "I LOVE PYTHON",
  e: kk,
  i: "62bs819idl00oac2",
  k: "0123456789abcdef"
}
console.log(b(data['r'], data['e']));

