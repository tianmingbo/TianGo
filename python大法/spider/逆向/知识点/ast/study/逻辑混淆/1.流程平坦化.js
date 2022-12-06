//target 流程平坦化
// Date.prototype.format = function (formatStr) {
//   let _array = '0|1|4|5|3|2'.split('|'), _index = 0;
//   while (!![]) {
//     switch (+_array[_index++]) {
//       case 0:
//         var str = formatStr;
//         continue;
//       case 1:
//         var Week = ['日', '一', '二', '三', '四', '五', '六'];
//         continue;
//       case 2:
//         return str;
//         continue;
//       case 3:
//         str = str.replace(/dd|DD/, this.getDate() > 9 ? (this.getDate() + 1).toString() : '0' + this.getDate());
//         continue;
//       case 4:
//         str = str.replace(/yyyy|YYYY/, this.getFullYear());
//         continue;
//       case 5:
//         str = str.replace(/MM/, (this.getMonth() + 1 > 9 ? (this.getMonth() + 1).toString() : '0' + (this.getMonth() + 1)))
//         continue;
//     }
//     break;
//   }
// }
//
// console.log(new Date().format('yyyy-MM-dd'));


const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./origin.js', {encoding: 'utf-8'})


let ast = parser.parse(jsCode);
traverse(ast, {
  FunctionExpression(path) {
    let blockStatement = path.node.body;
    let statements = blockStatement.body.map(function (v, i) {
      return {index: i, value: v};
    });
    let i = statements.length;
    while (i) {
      let j = Math.floor(Math.random() * i--);
      [statements[j], statements[i]] = [statements[i], statements[j]];
    }
    let dispenserArr = [];
    let cases = [];
    statements.map(function (v, i) {
      dispenserArr[v.index] = i;
      let switchCase = t.switchCase(t.numericLiteral(i), [v.value, t.continueStatement()]);
      cases.push(switchCase);
    });
    let dispenserStr = dispenserArr.join('|');
    let array = path.scope.generateUidIdentifier('array');
    let index = path.scope.generateUidIdentifier('index');
    let callee = t.memberExpression(t.stringLiteral(dispenserStr), t.identifier('split'));
    let arrayInit = t.callExpression(callee, [t.stringLiteral('|')]);
    let varArray = t.variableDeclarator(array, arrayInit);
    let varIndex = t.variableDeclarator(index, t.numericLiteral(0));
    let dispenser = t.variableDeclaration('let', [varArray, varIndex]);
    let uptExp = t.updateExpression('++', index);
    let memExp = t.memberExpression(array, uptExp, true);
    let discriminant = t.unaryExpression('+', memExp);
    let switchSta = t.switchStatement(discriminant, cases);
    let unaExp = t.unaryExpression('!', t.arrayExpression());
    unaExp = t.unaryExpression('!', unaExp);
    let whileSta = t.whileStatement(unaExp, t.blockStatement([switchSta, t.blockStatement()]))
    path.get('body').replaceWith(t.blockStatement([dispenser, whileSta]));
  }
})
let code = generator(ast).code;
fs.writeFile('./new2.js', code, (err) => {
});