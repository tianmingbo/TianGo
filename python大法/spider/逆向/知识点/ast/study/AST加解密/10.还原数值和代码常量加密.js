const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./res.js', {encoding: 'utf-8'})

let ast = parser.parse(jsCode);
traverse(ast, {
    //数值常量解密
    BinaryExpression(path) {
      let left = path.node.left;
      let right = path.node.right;
      if (t.isNumericLiteral(left) && t.isNumericLiteral(right)) {
        let {confident, value} = path.evaluate(); //confident代表节点是否可以计算出结果
        confident && path.replaceWith(t.valueToNode(value));
      }
    },
    //eval 解密
    CallExpression(path) {
      if (path.node.callee.name != 'eval') {
        return;
      }
      let arguments = path.node.arguments;
      let code = generator(arguments[0]).code; //判断eval中的参数是不是字符串
      if (t.isStringLiteral(arguments)) {
        //如果eval中的参数是StringLiteral节点，直接变成代码调用即可
        path.replaceWith(t.identifier(code));
      } else {
        //not就eval执行一遍再替换
        path.replaceWith(t.identifier(eval(code)));
      }
    }
  }
)

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});