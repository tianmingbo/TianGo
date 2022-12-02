const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

let a = t.identifier("a")
let left = t.numericLiteral(1000);
let right = t.numericLiteral(1000);
let bin = t.binaryExpression("+", left, right)
let varA = t.variableDeclarator(a, bin)
let _let = t.variableDeclaration('let', [varA]) //最后一步


let code = generator(_let).code;
fs.writeFile('./demoNew.js', code, (err) => {
});