//使用ast还原表达式
import {parse} from "@babel/parser"
import traverse from "@babel/traverse"
import generate from "@babel/generator"
import * as types from "@babel/types"

const code='const a=!![];const b="abc"=="bcd";const c=(1<<3)|2;const d=parseInt("5"+"0");'
let ast=parse(code);
traverse(ast,{
  //如果是一元表达式、布尔表达式、条件表达式、调用表达式，会执行以下方法
  "UnaryExpression|BinaryExpression|ConditionalExpression|CallExpression":(path)=>{
    //path.evaluate()计算表达式, confident表示可信度,可信为true
    const {confident,value}=path.evaluate();
    if(value==Infinity||value==-Infinity)return;
    //replaceWith把执行的结果进行替换
    confident && path.replaceWith(types.valueToNode(value));
  }
})
const {code:output}=generate(ast);
console.log(output)