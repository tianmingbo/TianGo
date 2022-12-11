const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;


const jsCode = fs.readFileSync('./test2.js', {encoding: 'utf-8'})

let ast = parser.parse(jsCode);

//得到解密函数所在节点
let stringDecryptFuncAst = ast.program.body[2];
//得到字符串解密函数的名字
let decryptFuncName = ast.program.body[3].declarations[0].id.name;

let newAst = parser.parse('');
newAst.program.body.push(ast.program.body[1]);
newAst.program.body.push(ast.program.body[2]);
//添加字符串解密函数
newAst.program.body.push(ast.program.body[3]);
newAst.program.body.push(stringDecryptFuncAst);
//生成时不能格式化代码，因为有格式化检测
let stringDecryptFunc = generator(newAst, {compact: true}).code;
eval(stringDecryptFunc);

//字符串解密
traverse(ast, {
  CallExpression(path) {
    if (path.node.callee.name === decryptFuncName) {
      console.log(generator(path.node).code)
      console.log(eval(generator(path.node).code + ''))
    }
  }
})
fs.writeFile('./ressss.js', stringDecryptFunc, (err) => {
});