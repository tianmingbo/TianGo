const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = 'Date.prototype.format = function (formatStr) {\n' +
  '  var str = formatStr;\n' +
  '  var Week = [\'日\', \'一\', \'二\', \'三\', \'四\', \'五\', \'六\'];\n' +
  '  str = str.replace(/yyyy|YYYY/, this.getFullYear());\n' +
  '  str = str.replace(/MM/, (this.getMonth() + 1 > 9 ? (this.getMonth() + 1).toString() : \'0\' + (this.getMonth() + 1)))\n' +
  '  str = str.replace(/dd|DD/, this.getDate() > 9 ? (this.getDate() + 1).toString() : \'0\' + this.getDate());\n' +
  '  return str;\n' +
  '}\n' +
  '\n' +
  'console.log(new Date().format(\'yyyy-MM-dd\'));'


let ast = parser.parse(jsCode);
traverse(ast, {
    FunctionExpression(path) {
      let blockStatement = path.node.body;
      let replaceStatement = blockStatement.body.map(function (v) {
        if (t.isReturnStatement(v)) {
          //return 语句不可加密
          return v;
        }
        let code = generator(v).code; //将语句变成字符串
        let cipherText = new Buffer(code).toString('base64');//base64编码
        let decryptFunc = t.callExpression(t.identifier('atob'), [t.stringLiteral(cipherText)]); //atob()
        return t.expressionStatement(t.callExpression(t.identifier('eval'), [decryptFunc])); //eval()
      });
      path.get('body').replaceWith(t.blockStatement(replaceStatement))
    }
  }
)
let code = generator(ast).code;
fs.writeFile('./new2.js', code, (err) => {
});