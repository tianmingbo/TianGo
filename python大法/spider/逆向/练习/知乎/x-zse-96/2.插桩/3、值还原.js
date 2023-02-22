const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./jsvmp2.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
// this.M[21] = 8;是个定值，其他地方没有赋值
//{ '0': 66, '11': 68, '15': 16, '18': 134, '21': 8, '26': 52 }
let cases_dict = {};
// 数组虚假分析
traverse(ast, {
  MemberExpression(path) {
    //path.parent是Node，path.parentPath是父级Path
    if (path.node.object.type === 'ThisExpression' && path.node.property.type === 'Identifier' && path.node.property.name === 'M' && path.parent.type === 'MemberExpression') {
      if (path.parentPath.parent.type === 'AssignmentExpression' && path.parentPath.parent.right.type === 'NumericLiteral') {
        cases_dict[path.parent.property.value] = path.parentPath.parent.right.value;
        path.parentPath.parentPath.remove()
      }
    }
  }
});
traverse(ast, {
  MemberExpression(path) {
    //替换为常量
    if (path.node.object.type === 'ThisExpression' && path.node.property.type === 'Identifier' && path.node.property.name === 'M' && path.parent.type === 'MemberExpression') {
      if (cases_dict.hasOwnProperty(path.parent.property.value)) {
        path.parentPath.replaceWith(t.numericLiteral(cases_dict[path.parent.property.value]))
      } else {
        path.parentPath.replaceWith(t.numericLiteral(0))
      }
    }
  }
});

let code = generator(ast).code;
fs.writeFile('./jsvmp3.js', code, (err) => {
});
