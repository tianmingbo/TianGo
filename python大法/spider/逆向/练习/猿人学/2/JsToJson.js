// JsToJson.js
// js 转 json 
const fs = require('fs');
const esprima = require('esprima')
const escodegen = require('escodegen')

const input_text = process.argv[2];
const output_text = process.argv[3];

const data = fs.readFileSync(input_text);
const ast = esprima.parseScript(data.toString());
const ast_to_json = JSON.stringify(ast);
fs.writeFileSync(output_text, ast_to_json);

