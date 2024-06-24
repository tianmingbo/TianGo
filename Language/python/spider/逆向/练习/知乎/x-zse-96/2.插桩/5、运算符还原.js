const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./jsvmp4.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
//this.T = 5 * 80 - 48=352
traverse(ast, {
  SwitchCase(path) {
    if (path.node.test) {
      if (path.node.consequent[path.node.consequent.length - 2].expression.right.type === 'NumericLiteral') {
        if (path.node.consequent[path.node.consequent.length - 2].expression.operator === '+=') {
          path.node.consequent[path.node.consequent.length - 2].expression.operator = '=';
          path.node.consequent[path.node.consequent.length - 2].expression.right.value = path.node.consequent[path.node.consequent.length - 2].expression.right.value + path.node.test.value;
        } else if (path.node.consequent[path.node.consequent.length - 2].expression.operator === '-=') {
          path.node.consequent[path.node.consequent.length - 2].expression.operator = '=';
          path.node.consequent[path.node.consequent.length - 2].expression.right.value = path.node.test.value - path.node.consequent[path.node.consequent.length - 2].expression.right.value;
        }
      }
    }
  }, "BinaryExpression"(path) {
    let left = path.node.left;
    let right = path.node.right;
    if (left.type == "NumericLiteral" | left.type == "UnaryExpression" && right.type == "NumericLiteral" | right.type == "UnaryExpression") {
      path.replaceWith(t.valueToNode(path.evaluate().value));
    }
  }
});

let code = generator(ast).code;
fs.writeFile('./jsvmp5.js', code, (err) => {
});
