const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = 'let obj = {\n' +
  '  name: "tiandali",\n' +
  '  add: function (a, b) {\n' +
  '    return a + b + 100;\n' +
  '  },\n' +
  '  mul: function (a, b) {\n' +
  '    return a * b + 10000;\n' +
  '  }\n' +
  '}'

let ast = parser.parse(jsCode);
// let visitor = {}
// visitor.FunctionExpression = function (path) {
//   console.log("tmb")
// }

//多个函数应用于同一个节点
const visitor = {
  "FunctionExpression|BinaryExpression": {
    enter(path) {
      console.log(path.node.name)
    },
    exit(path) {
      console.log(path.type)
    }
  }
}
traverse(ast, visitor)

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});