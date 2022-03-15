//使用ast反控制流平坦化
import {parse} from "@babel/parser"
import traverse from "@babel/traverse"
import generate from "@babel/generator"
import * as types from "@babel/types"

let code='const s=\'3|1|2\'.split(\'|\')\n' +
  'let x=0;\n' +
  'while (true){\n' +
  '  switch (s[x++]){\n' +
  '    case \'1\':\n' +
  '      const a=1;\n' +
  '      continue;\n' +
  '    case \'2\':\n' +
  '      const b=2;\n' +
  '      continue\n' +
  '    case \'3\':\n' +
  '      const c=3;\n' +
  '      continue\n' +
  '  }\n' +
  '  break\n' +
  '}'

let ast=parse(code)
traverse(ast,{

})
console.log(code)