const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');

const jscode = fs.readFileSync("./res0.js", {
  encoding: "utf-8"
});

let ast = parser.parse(jscode);

///////////去除数组混淆

//拿到解密函数所在节点
let stringDecryptFuncAst = ast.program.body[2];
//拿到解密函数的名字
let DecryptFuncName = stringDecryptFuncAst.declarations[0].id.name;
//新建一个 AST，把原代码中的前三部分，加入到 body 节点中
let newAst = parser.parse('');
newAst.program.body.push(ast.program.body[0]);
newAst.program.body.push(ast.program.body[1]);
newAst.program.body.push(stringDecryptFuncAst);
//把这三部分的代码转为字符串，由于存在格式化检测，需要指定选项，来压缩代码
let stringDecryptFunc = generator(newAst, {compact: true}).code;
//将字符串形式的代码执行，这样就可以在 nodejs 中运行解密函数了
eval(stringDecryptFunc);

traverse(ast, {
  //////字符串解密
  //遍历所有变量
  VariableDeclarator(path) {
    //当变量名与解密函数名相同时，就执行相应操作
    if (path.node.id.name === DecryptFuncName) {
      let binding = path.scope.getBinding(DecryptFuncName);
      binding && binding.referencePaths.map(function (v) {
        v.parentPath.isCallExpression() &&
        v.parentPath.replaceWith(t.stringLiteral(eval(v.parentPath + '')));

      });
    }
  }
});

ast.program.body.shift();
ast.program.body.shift();
ast.program.body.shift();

let code = generator(ast).code;
fs.writeFile('./res1.js', code, (err) => {
});
