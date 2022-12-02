const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./demo.js', {encoding: 'utf-8'})

let ast = parser.parse(jsCode);
traverse(ast, {
  Identifier(path) {
    //给js内置对象加上window
    let name = path.node.name;
    if ('eval|Date|parseInt|Function|Boolean|Number|Math|String|RegExp|Array|Object'.indexOf(name) !== -1) {
      path.replaceWith(t.memberExpression(t.identifier('window'), t.identifier(name), true));
    }
  },
  MemberExpression(path) {
    //console.log替换成console['log']
    if (t.isIdentifier(path.node.property)) {
      let name = path.node.property.name;
      path.node.property = t.stringLiteral(name);
    }
    path.node.computed = true;
  }
})

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});