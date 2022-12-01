/**
 * scope可以方便的查找标识符的作用域，获取并修改标识符的所有引用，以及判断
 * 标识符是否为参数或常量
 * */

// const a = 1000;
// let b = 2000;
// let obj = {
//   name: 'dali',
//   add: function (a) {
//     a = 400;
//     b = 300;
//     let e = 700;
//
//     function demo() {
//       let d = 600;
//     }
//
//     demo();
//     return a + a + b + 1000 + obj.name;
//   }
// }
// obj.add(100)


const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = 'const a = 1000;\n' +
  'let b = 2000;\n' +
  'let obj = {\n' +
  '  name: \'dali\',\n' +
  '  add: function (a) {\n' +
  '    a = 400;\n' +
  '    b = 300;\n' +
  '    let e = 700;\n' +
  '\n' +
  '    function demo() {\n' +
  '      let d = 600;\n' +
  '    }\n' +
  '\n' +
  '    demo();\n' +
  '    return a + a + b + 1000 + obj.name;\n' +
  '  }\n' +
  '}\n' +
  'obj.add(100)'

let ast = parser.parse(jsCode);
traverse(ast, {
  Identifier(path) {
    if (path.node.name === 'e') {
      console.log(generator(path.scope.block).code) //输出变量e的作用域
      console.log('**********')
    }
    // path.scope.rename(path.node.name, path.scope.generateUidIdentifier('_0xabcd').name)  //标识符混淆
  }, FunctionDeclaration(path) {
    console.log(generator(path.scope.parent.block).code)
    console.log('**********')
    let bindA = path.scope.getBinding('a'); //getBinding 获取对应标识符的绑定
    console.log(generator(bindA.scope.block).code);//功能同上
    console.log('**********')
    let bindDemo = path.scope.getBinding('demo');
    console.log(generator(bindDemo.scope.block).code);//功能同上
    console.log('**********');
    //遍历作用域
    bindA.scope.traverse(bindA.scope.block, {
      AssignmentExpression(path) {
        if (path.node.left.name === 'a') {
          path.node.right = t.numericLiteral(666);
        }
      }
    })
    console.log('**********');
    bindA.scope.rename("aaa"); //重命名
  }
})
let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});