const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./jsvmp3.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
// 还原this.T成常量
traverse(ast, {
  SwitchCase(path) {
    if (path.node.test) {
      if (path.node.consequent.length > 1 && path.node.consequent[path.node.consequent.length - 2].expression.right.type === 'BinaryExpression') {
        let item = path.node.consequent[path.node.consequent.length - 2].expression.right;
        if (item.left.type === 'BinaryExpression' && item.left.right.type === 'MemberExpression' && item.left.right.property.type === 'Identifier' && item.left.right.property.name === 'T') {
          item.left.right = t.numericLiteral(path.node.test.value); //case 的值就是this.T的值
        }
      }
    }
  }
});

let code = generator(ast).code;
fs.writeFile('./jsvmp4.js', code, (err) => {
});
