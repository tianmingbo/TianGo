const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = 'function test(a,b){\n' +
  'return c=a,d=b+3;\n' +
  '}'

let ast = parser.parse(jsCode);
traverse(ast, {
    SequenceExpression: {
      exit(path) {
        let expressions = path.node.expressions;
        let finalExpression = expressions.pop();
        let statement = path.getStatementParent();
        expressions.map(function (v) {
          statement.insertBefore(t.ExpressionStatement(v));
        })
        path.replaceInline(finalExpression);
      }
    }
  }
)

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});