const code = `
let x='1'+1;
console.log('x',x)
`
const options = {
    compact: false,
    controlFlowFlattening: true
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))