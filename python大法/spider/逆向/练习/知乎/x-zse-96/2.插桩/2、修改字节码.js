const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./demo.js', {encoding: 'utf-8'})

//生成ast
let ast = parser.parse(jsCode);
//在这里对AST操作

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});