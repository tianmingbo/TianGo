// JsonToJs.js
// json 转 js
const fs = require('fs');
const esprima = require('esprima')
const escodegen = require('escodegen')

const input_text = process.argv[2];
const output_text = process.argv[3];

const data = fs.readFileSync(input_text);
const ast = JSON.parse(data.toString());
const code = escodegen.generate(ast, {
    format: {
        compact: true,
        escapeless: true
    }
});
fs.writeFileSync(output_text, code);

