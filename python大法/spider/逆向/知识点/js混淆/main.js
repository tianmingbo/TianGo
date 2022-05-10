const code = `
console.log('chendali')
`
const options = {
  compact: true, //代码压缩
  controlFlowFlattening: true, //控制流平坦化
  identifierNamesGenerator:'mangled', //变量名混淆
  unicodeEscapeSequence:true,//unicode编码
  selfDefending:true,//代码自我保护，不能格式化，格式化会卡死
  deadCodeInjection:true,//无用代码注入
  transformObjectKeys:true,//对象键名替换
  disableConsoleOutput:true,//禁用控制台输出

}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
  return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))