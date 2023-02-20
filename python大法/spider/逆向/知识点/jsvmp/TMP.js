const CryptoJS = require("crypto-js");

function AESencrypt(data, key, iv) { //key,iv：16位的字符串
    var key1 = CryptoJS.enc.Utf8.parse(key);
    var iv1 = CryptoJS.enc.Utf8.parse(iv);
    return CryptoJS.AES.encrypt(data, key1, {
        iv: iv1,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString();
}

t = 1676888065
page = 2
var key = iv = t.toString(16) + t.toString(16)
data = page.toString() + "|" + "179d335,179d335,179u335,179u335"
res = AESencrypt(data, key, iv)
console.log(res)