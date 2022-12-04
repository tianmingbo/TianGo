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

function generateIdentifier(decNum) {
  //标识符替换
  let flag = ['O', 'o', '0'];
  let retVal = [];
  while (decNum > 0) {
    retVal.push(decNum % 3);
    decNum = parseInt(decNum / 3);
  }
  let Identifier = retVal.reverse().map(function (v) {
    return flag[v];
  }).join('');
  Identifier.length < 6 ? (Identifier = ('OOOOOO' + Identifier).substr(-6)) :
    Identifier[0] === '0' && (Identifier = 'O' + Identifier);
  return Identifier;
}

function renameOwnBinding(path) {
  let ownBinding = {}, globalBinding = {}, i = 0;
  path.traverse({
    Identifier(p) {
      let name = p.node.name;
      let binding = p.scope.getOwnBinding(name);
      binding && generator(binding.scope.block).code == path + '' ?
        (ownBinding[name] = binding) : (globalBinding[name] = 1);
    }
  });
  for (let oldName in ownBinding) {
    do {
      var newName = generateIdentifier(i++);
    } while (globalBinding[newName]);
    ownBinding[oldName].scope.rename(oldName, newName);
  }
}

let ast = parser.parse(jsCode);
traverse(ast, {
  'Program|FunctionExpression|FunctionDeclaration'(path) {
    renameOwnBinding(path);
  }
})
let code = generator(ast).code;
fs.writeFile('./new2.js', code, (err) => {
});