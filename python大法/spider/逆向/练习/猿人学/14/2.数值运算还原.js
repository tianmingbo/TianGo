const fs = require('fs');
//js转AST代码
const parser = require('@babel/parser');
//遍历ASR节点
const traverse = require('@babel/traverse').default;
//用来判断节点类型产生新的节点
const t = require('@babel/types');
//用来把AST转换成js代码
const generator = require('@babel/generator').default;
const jscode = fs.readFileSync("./mz1.js", {
  encoding: "utf-8"
});

const visitor = {
  "BinaryExpression"(path) {
    let left = path.node.left;
    let right = path.node.right;
    if (left.type == "NumericLiteral" | left.type == "UnaryExpression" && right.type == "NumericLiteral" | right.type == "UnaryExpression") {
      path.replaceWith(t.valueToNode(path.evaluate().value));
    }
  }
}

const revertUnaryExpression = {
  "UnaryExpression"(path) {
    let argument = path.node.argument;
    if (argument.type == 'NumericLiteral' | argument.type == 'UnaryExpression' && generator(path.node).code.indexOf(' -') != -1) {
      path.replaceWith(t.valueToNode(eval(generator(path.node).code)));
    }
  }
}
let ast = parser.parse(jscode);
for (let i = 0; i < 10; i++) {
  traverse(ast, visitor);
}
traverse(ast, revertUnaryExpression)

let code = generator(ast).code;
fs.writeFile('./mz2.js', code, (err) => {
});