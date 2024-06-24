// 字符串转char code
function stringToCharCode(str) {
  let move = [0, 8, 16, 24]
  let orChar = 0, charCode;
  for (let m of move) {
    let i = move.indexOf(m)
    charCode = str.charCodeAt.apply(str, [i]) << m | orChar;
    orChar = charCode;
  }
  return charCode;
}

function strToLongs(s) {
  let l = new Array(Math.ceil(s.length / 4));
  for (let i = 0; i < l.length; i++) {
    l[i] = s.charCodeAt(i * 4) + (s.charCodeAt(i * 4 + 1) << 8) +
      (s.charCodeAt(i * 4 + 2) << 16) + (s.charCodeAt(i * 4 + 3) << 24);
  }
  return l;
}

function EncryptBlock(v) {
  let key = [1464165968, 1346793039, 1782794837, 1198157381];
  let l = v[0], r = v[1]
  let sum = 0;
  let delta = 2654435769;
  for (let i = 0; i < 32; i++) {
    l += (((r << 4) ^ (r >>> 5)) + r) ^ (sum + key[sum & 3]);
    sum += delta;
    r += (((l << 4) ^ (l >>> 5)) + l) ^ (sum + key[(sum >>> 11) & 3]);
  }
  return [l, r];
}

function DecryptBlock(v) {
  let key = [1464165968, 1346793039, 1782794837, 1198157381];
  let l = v[0], r = v[1]
  let sum = 2654435769 * 32;
  let delta = 2654435769;
  for (let i = 0; i < 32; i++) {
    r -= (((l << 4) ^ (l >>> 5)) + l) ^ (sum + key[(sum >>> 11) & 3]);
    sum -= delta;
    l -= (((r << 4) ^ (r >>> 5)) + r) ^ (sum + key[sum & 3]);

  }
  return [l, r];
}

// 第三步：编码转换unicode
function stringToUnicode(char) {
  let move = [0, 8, 16, 24];
  let unicodes = [];
  for (let m of move) {
    let code = char >> m & 255;
    unicodes.push(code);
  }
  return String.fromCharCode.apply(String, unicodes);
}

function longsToStr(l) {
  let a = new Array(l.length);
  for (let i = 0; i < l.length; i++) {
    a[i] = String.fromCharCode(l[i] & 0xFF, l[i] >> 8 & 0xFF,
      l[i] >> 16 & 0xFF, l[i] >> 24 & 0xFF);
  }
  return a.join('');
}

let str1 = '{"cd":[101000,"Google Inc. (Intel Inc.)",8,"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36","7039406035871428608","iframe",3720,1678325185,1678325378,1,                 '
let str3 = ',"",900,0,"UTF-8","ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics OpenGL Engine, OpenGL 4.1)","",486763870,1626788935,[],0,[360,360],"MacIntel",2,1023,2,["zh-CN","zh"],"98k",30,3.884000062942505,"1440-900-875-30-*-*-|-*","https://007.qq.com/?rand=1512991986334","GgoAAAANSUhEUgAAASwAAACWCAYAAABlQZMm3+6TNvS2WJ0S9+/vPrJe3e1HT+F1ANih5hSMVDAAAAAElFTkSuQmCC","https://t.captcha.qq.com/cap_union_new_show?rand=1519713624347","+08",1858764808,1440,92070],   '
let str2 = '[[346,166,45520],[-32,14,7],[-14,5,9],[-9,4,8],[-20,8,8],[-15,6,9],[-12,3,11],[-4,1,4],[-6,2,9],[-5,1,9],[-4,0,7],[-2,0,8],[-4,1,8],[-1,0,8],[-2,0,9],[-3,0,7],[-1,0,9],[-2,0,8],[-2,1,7],[-1,0,8],[-2,0,9],[-1,0,9],[-2,0,8],[-2,0,8],[-2,0,8],[-2,1,7],[-2,0,8],[-1,0,8],[-2,1,8],[-2,0,9],[-3,1,8],[-2,1,7],[-2,1,8],[-2,1,11],[-3,2,6],[-3,2,9],[-3,2,9],[-3,3,6],[-5,3,9],[-4,4,7],[-4,3,8],[-4,4,8],[-4,3,9],[-3,4,11],[-5,4,5],[-4,3,8],[-3,4,8],[-4,3,8],[-3,3,8],[-1,1,8],[-2,2,10],[-3,2,6],[-2,1,8],[-2,2,9],[-1,1,8],[-2,0,8],[-2,2,9],[-1,0,8],[-2,1,7],[-2,1,8],[1,1,12]]         '
let str4 = '"sd":{"od":"C","clientType":"","coordinate":[10,64,0.5015],"trycnt":2,"refreshcnt":1,"slideValue":[[83,287,107],[4,0,16],[5,0,6],[8,0,17],[15,0,16],[19,0,16],[17,0,16],[15,0,17],[14,0,16],[9,0,17],[15,3,40],[7,2,7],[5,1,17],[5,1,18],[3,1,17],[2,1,16],[1,1,16],[0,0,0]],"dragobj":1,"ft":"qf_7P_n_H"}}'

function teaEncrypt(str) {
  let res = '';
  for (let i = 0; i < str.length; i += 8) {
    let encryptStr = str.slice(i, i + 8);
    let l = stringToCharCode(encryptStr.slice(0, 4));
    let r = stringToCharCode(encryptStr.slice(4, 8));
    let teaEncryptRes = EncryptBlock([l, r])
    res = res + stringToUnicode(teaEncryptRes[0]) + stringToUnicode(teaEncryptRes[1])
  }
  return res;
}

function teaDecrypt(msg) {
  let decryptStr = atob(msg);
  let tmp;
  let res = "";
  for (let i = 0; i < decryptStr.length; i += 8) {
    tmp = DecryptBlock(strToLongs(decryptStr.slice(i, i + 8)));
    res += longsToStr(tmp);
  }
  return res;
}


// console.log(btoa(teaEncrypt(str1) + teaEncrypt(str2) + teaEncrypt(str3) + teaEncrypt(str4)))
console.log(teaDecrypt('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'))

// TODO
/**
 * 1. key不固定，delta固定为2654435769
 * 2. 参数来源不清晰
 * 3. vdata
 * */