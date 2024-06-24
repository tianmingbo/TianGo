//traverse 用来遍历AST对象
import {parse} from "@babel/parser"
import traverse from "@babel/traverse"
import generate from "@babel/generator"
import fs from "fs";

const code=fs.readFileSync('demo.js','utf-8')
let ast=parse(code);
traverse(ast,{
  //遇到NumericLiteral节点自动调用对应的方法
Literal(path){
  if(path.node.value===3){
    path.node.value=5;
  }
},
  StringLiteral(path){
  if(path.node.value==='hello'){
    path.node.value='hi';
  }
  },
  CallExpression(path) {
    let node =path.node;
    if(node.callee.object.name==='console' && node.callee.property.name==='log'){
      path.remove();//移除代码
    }
}
});
const {code:output}=generate(ast,{retainLines:true});
console.log(output);