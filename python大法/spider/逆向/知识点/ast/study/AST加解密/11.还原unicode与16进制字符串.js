const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;

const jsCode = fs.readFileSync('./test.js', {encoding: 'utf-8'})

let ast = parser.parse(jsCode);//parse 一下就可以了

let code = generator(ast, {minified: true, jsescOption: {minimum: true}}).code;
ast = parser.parse(code);
code = generator(ast).code;
fs.writeFile('./test2.js', code, (err) => {
});