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
    let blockStatementLength = blockStatement.body.length;
    if (blockStatementLength < 2) {
      return;
    }
    //把变量的声明提到参数列表中
    path.traverse({
      VariableDeclaration(p) {
        let declarations = p.node.declarations;
        let statements = [];
        declarations.map(function (v) {
          path.node.params.push(v.id);
          v.init && statements.push(t.assignmentExpression('=', v.id, v.init))
        })
      }
    });
    /*
    * 未理解
    * */
  }
})
let code = generator(ast).code;
fs.writeFile('./new2.js', code, (err) => {
});