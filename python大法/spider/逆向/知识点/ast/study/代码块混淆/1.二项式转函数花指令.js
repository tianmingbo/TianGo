// Date.prototype.format = function (formatStr) {
//   var str = formatStr;
//   var Week = ['日', '一', '二', '三', '四', '五', '六'];
//   str = str.replace(/yyyy|YYYY/, this.getFullYear());
//   str = str.replace(/MM/, (this.getMonth() + 1 > 9 ? (this.getMonth() + 1).toString() : '0' + (this.getMonth() + 1)))
//   str = str.replace(/dd|DD/, this.getDate() > 9 ? (this.getDate() + 1).toString() : '0' + this.getDate());
//   return str;
// }
//
// console.log(new Date().format('yyyy-MM-dd'));
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
    BinaryExpression(path) {
      let operator = path.node.operator;
      let left = path.node.left;
      let right = path.node.right;
      let a = t.identifier('a');
      let b = t.identifier('b');
      let functionIdentifier = path.scope.generateUidIdentifier('xxx');
      //构建函数
      let func = t.functionDeclaration(functionIdentifier, [a, b],
        t.blockStatement([t.returnStatement(t.binaryExpression(operator, a, b))]));

      let blockStatement = path.findParent(function (p) {
        return p.isBlockStatement()
      });
      //把生成的函数放到最前面
      blockStatement.node.body.unshift(func);
      //替换原来的代码
      path.replaceWith(t.callExpression(functionIdentifier, [left, right]));
    }
  }
)
let code = generator(ast).code;
fs.writeFile('./new2.js', code, (err) => {
});