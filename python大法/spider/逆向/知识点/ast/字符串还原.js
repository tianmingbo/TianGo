//使用AST还原表达式
import {parse} from "@babel/parser"
import traverse from "@babel/traverse"
import generate from "@babel/generator"

const code='const strings=["\x68\x65\x6c\x6c\x6f"]'
let ast =parse(code);
traverse(ast,{
  StringLiteral({node}){
    if(node.extra && /\\[ux]/gi.test(node.extra.raw)){
      node.extra.raw=node.extra.rawValue;
    }
  }
});
const {code:output}=generate(ast);
console.log(output);