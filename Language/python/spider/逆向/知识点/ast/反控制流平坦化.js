//使用ast反控制流平坦化
//https://astexplorer.net/
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
WhileStatement(path){
  const {node,scope}=path;
  const {body}=node;
  let switchNode=body.body[0];  //获取switch块
  let {discriminant,cases}=switchNode; //discriminant是判定条件, cases是case块
  let {object}=discriminant; //获取判断条件中的值，即s对象
  let arrName=object.name; //获取name,即s
  let binding=scope.getBinding(arrName);//获取s绑定的对象,即'3|1|2'.split('|')
  let {init}=binding.path.node;//获取snode
  object=init.callee.object; //获取3|1|2
  let propertyName=init.callee.property.name; //获取split
  let argument=init.arguments[0].value; //获取运算符 |
  let arrayFlow=object.value[propertyName](argument); //执行运算 ,获得['3','1','2']
  let resultBody=[];
  arrayFlow.forEach((index)=>{
    //循环case的value等于index值
    let switchCase=cases.filter((c)=>c.test.value===index)[0];
    let caseBody=switchCase.consequent;//case块
    if(types.isContinueStatement(caseBody[caseBody.length-1])){
      //如果是continue块
      caseBody.pop();
    }
    resultBody=resultBody.concat(caseBody); //追加
  })
  path.replaceWithMultiple(resultBody); //替换switch case
}
})
const {code:output}=generate(ast);
console.log(output);