const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./jsvmp.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
// 删除时间参数 this.a 干掉时间检测
traverse(ast, {
  SwitchCase(path) {
    if (path.node.test) {
      if (path.node.test.value === 300) {
        path.node.consequent.splice(0, 1)
      } else if (path.node.test.value === 360) {
        path.node.consequent.splice(0, 1)
      } else if (path.node.test.value === 368) {
        path.node.consequent[0].expression.right.test = t.booleanLiteral(false)
      }
    }
  },
  // FunctionDeclaration(path) {
  //   if (path.node.id && path.node.id.name === 'l') {
  //     for (let i = path.node.body.body.length - 1; i >= 0; i--) {
  //       let item = path.node.body.body[i];
  //       if (item.expression.left.property.name === 'a' || item.expression.left.property.name === 'U') {
  //         path.node.body.body.splice(i, 1)
  //       }
  //     }
  //   }
  // }
});
let code = generator(ast).code;
fs.writeFile('./jsvmp1.js', code, (err) => {
});
