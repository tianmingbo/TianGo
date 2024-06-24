const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

let ast = parser.parse('function test(a) {\n' +
  '  return a + 100;\n' +
  '}');

traverse(ast, {
  ReturnStatement(path) {
    let argumentPath = path.get('argument');
    argumentPath.replaceWithSourceString('function(){return a+1000}()');
    path.stop();

  }
})
let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});