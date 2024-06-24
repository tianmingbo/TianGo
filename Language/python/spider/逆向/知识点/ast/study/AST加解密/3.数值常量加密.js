const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = fs.readFileSync('./demoNew.js', {encoding: 'utf-8'})
/* before：
  str = str["replace"](/MM/, this["getMonth"]() + 1 > 9 ? (this["getMonth"]() + 1)["toString"]() : '0' + (this["getMonth"]() + 1));
  str = str["replace"](/dd|DD/, this["getDate"]() > 9 ? (this["getDate"]() + 1)["toString"]() : '0' + this["getDate"]());
};
* */
let ast = parser.parse(jsCode);
traverse(ast, {
  NumericLiteral(path) {
    let value = path.node.value;
    let key = parseInt(Math.random() * (999999 - 100000) + 100000, 10);
    let cipherNum = value ^ key;
    path.replaceWith(t.binaryExpression('^', t.numericLiteral(cipherNum), t.numericLiteral(key)));
    path.skip();
  }
})

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});

/*after:

* str = str["replace"](/MM/, this["getMonth"]() + (915611 ^ 915610) > (535403 ^ 535394) ? (this["getMonth"]() + (281720 ^ 281721))["toString"]() : '0' + (this["getMonth"]() + (956931 ^ 956930)));
  str = str["replace"](/dd|DD/, this["getDate"]() > (651014 ^ 651023) ? (this["getDate"]() + (215051 ^ 215050))["toString"]() : '0' + this["getDate"]());
* */