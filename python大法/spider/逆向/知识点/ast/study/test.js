const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

var left = t.identifier("a");
var right = t.numericLiteral(100);
var binary = t.binaryExpression('+', left, right)
var returnment = t.returnStatement(binary);
var block = t.blockStatement([returnment])
var para = t.identifier('a');
var funName = t.identifier('test');
var fun = t.functionDeclaration(funName, [para], block);
let code = generator(fun).code;
fs.writeFile('./demoNew.js', code, (err) => {
});