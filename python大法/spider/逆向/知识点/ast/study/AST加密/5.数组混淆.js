const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;


var Base64 = {
  _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

  encode: function (e) {
    var t = "";
    var n, r, i, s, o, u, a;
    var f = 0;
    e = Base64._utf8_encode(e);
    while (f < e.length) {
      n = e.charCodeAt(f++);
      r = e.charCodeAt(f++);
      i = e.charCodeAt(f++);
      s = n >> 2;
      o = (n & 3) << 4 | r >> 4;
      u = (r & 15) << 2 | i >> 6;
      a = i & 63;
      if (isNaN(r)) {
        u = a = 64
      } else if (isNaN(i)) {
        a = 64
      }
      t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
    }
    return t
  },

  _utf8_encode: function (e) {
    e = e.replace(/rn/g, "n");
    var t = "";
    for (var n = 0; n < e.length; n++) {
      var r = e.charCodeAt(n);
      if (r < 128) {
        t += String.fromCharCode(r)
      } else if (r > 127 && r < 2048) {
        t += String.fromCharCode(r >> 6 | 192);
        t += String.fromCharCode(r & 63 | 128)
      } else {
        t += String.fromCharCode(r >> 12 | 224);
        t += String.fromCharCode(r >> 6 & 63 | 128);
        t += String.fromCharCode(r & 63 | 128)
      }
    }
    return t
  }
}


//以上是base64实现

const jsCode = fs.readFileSync('./demoNew.js', {encoding: 'utf-8'})
let ast = parser.parse(jsCode);
let bigArr = [];
traverse(ast, {
  StringLiteral(path) {
    let cipherText = Base64.encode(path.node.value);
    let index = bigArr.indexOf(cipherText);
    if (index === -1) {
      let length = bigArr.push(cipherText); //Push会返回加入成员以后的长度
      index = length - 1;
    }
    let encStr = t.callExpression(t.identifier('atob'), [t.memberExpression(t.identifier('arr'), t.numericLiteral(index), true)]); //替换成atob(arr[0])
    path.replaceWith(encStr);
  }
})
bigArr = bigArr.map(function (v) {
  return t.stringLiteral(v);
})
bigArr = t.variableDeclarator(t.identifier('arr'), t.arrayExpression(bigArr));
bigArr = t.variableDeclaration('var', [bigArr]);
ast.program.body.unshift(bigArr);//把bigArr加到最前面

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});
