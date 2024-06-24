const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./jsvmp1.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
// 删除不会走到的流程
let cases_list = [27, 34, 41, 48, 101, 117, 124, 147, 258, 283, 380, 400, 449, 459, 468, 469, 473, 479, 481, 485, 491, 496, 506];
traverse(ast, {
  SwitchCase(path) {
    if (path.node.test) {
      if (cases_list.includes(path.node.test.value)) {
        path.remove()
      }
    }
  }
});
let code = generator(ast).code;
fs.writeFile('./jsvmp2.js', code, (err) => {
});
