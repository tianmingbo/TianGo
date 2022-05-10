//使用ast剔除无用代码
import {parse} from "@babel/parser"
import traverse from "@babel/traverse"
import generate from "@babel/generator"
import * as types from "@babel/types"

let code='const _0x16c18d=function () {\n' +
  '  if(!![[]]){\n' +
  '    console.log(\'hello\')\n' +
  '  }else{\n' +
  '    console.log(\'nothing\')\n' +
  '  }\n' +
  '}\n' +
  'const _0x1f7292=function(){\n' +
  '  if(\'xmv2ndafdkjhf\'.charAt(4)!==String.fromCharCode(110)){\n' +
  '    console.log(\'nothing\')\n' +
  '  }else{\n' +
  '    console.log(\'nice\')\n' +
  '  }\n' +
  '}\n' +
  '\n' +
  '_0x1f7292()\n' +
  '_0x16c18d()'
let ast=parse(code);
traverse(ast,{
  IfStatement(path) {
    //consequent是if代码段,alternate是else代码段
    let {consequent,alternate}=path.node;
    //test是if判断语句
    let testPath=path.get('test');
    //evaluateTruthy()获得判断语句的 真值 t|f
    const evaluateTest=testPath.evaluateTruthy();
    if(evaluateTest===true){
      //如果是真值
      if(types.isBlockStatement(consequent)){
        consequent=consequent.body;
      }
      //直接替换
      path.replaceWithMultiple(consequent);
    }else if(evaluateTest===false){
      if(alternate!=null){
        if(types.isBlockStatement(alternate)){
          alternate=alternate.body;
        }
        path.replaceWithMultiple(alternate);
      }
    }else{
      //如果啥都不是,直接删除
      path.remove();
    }
  }
})
const {code:output}=generate(ast,{retainLines:true});
console.log(output);