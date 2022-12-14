const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');

const jscode = fs.readFileSync("./res2.js", {
  encoding: "utf-8"
});


let ast = parser.parse(jscode);
var totalObj = {};

function generateObj(ast) {
  //解析原始代码中的ObjectExpression节点，
  traverse(ast, {
    VariableDeclarator(path) {
      //init 节点为 ObjectExpression 的时候，就是需要处理的对象
      if (t.isObjectExpression(path.node.init)) {
        //取出对象名
        let objName = path.node.id.name;
        //以对象名作为属性名在 totalObj 中创建对象
        objName && (totalObj[objName] = totalObj[objName] || {});
        //解析对象中的每一个属性，加入到新建的对象中去，注意属性值依然是 Node 类型
        totalObj[objName] && path.node.init.properties.map(function (p) {
          totalObj[objName][p.key.value] = p.value;
        });
      }
    }
  });
  return ast;
}

function findRealFunc(node) {
  //ObjectProperty中有三种类型,以下处理FunctionExpression类型
  //(1)筛选FunctionExpression，且函数体只有一行代码，其余节点直接返回原节点
  if (t.isFunctionExpression(node) && node.body.body.length === 1) {
    //(2)取出ReturnStatement节点的argument属性中的callee
    let expr = node.body.body[0].argument.callee; //如果expr不是callee类型，说明就是所需要的节点，如    'ZFmTI': function (_0x4e4bbb, _0x19e1fa) return _0x4e4bbb + _0x19e1fa;
    //(4)如果第二步取出的undefined,说明已经是最后所需要的节点,如 return _0x1235a9 != _0x38f538; 直接返回即可
    if (t.isMemberExpression(expr)) {
      /**
       * (3)如果第二步取出的是MemberExpression,就取出对象名和属性名,从totalObj中获取对应的节点,进行递归
       * 处理如下类型
       * 'kfqzC': function (_0x56e39c, _0x1a2cd7) {
       *   return _0x1f20d3["PrDEx"](_0x56e39c, _0x1a2cd7);
          },
       * */
      let objName = expr.object.name;
      let propName = expr.property.value;
      if (totalObj[objName]) {
        return findRealFunc(totalObj[objName][propName]);
      } else {
        return false;
      }
    }
  } else {
    return node;
  }
}

ast = generateObj(ast);

traverse(ast, {
  VariableDeclarator(path) {
    if (t.isObjectExpression(path.node.init)) {
      path.node.init.properties.map(function (p) {
        let realNode = findRealFunc(p.value);
        realNode && (p.value = realNode); //进行节点替换
      })
    }
  }
})

ast = generateObj(ast); //更新totalObj对象

//替换使用函数花指令的地方，如_0x3fe98e["rxSBM"](_0x104aba["length"], 0x0)
traverse(ast, {
  CallExpression(path) {
    //callee 不为MemberExpression的不处理
    if (!t.isMemberExpression(path.node.callee)) return;
    let objName = path.node.callee.object.name;
    let propName = path.node.callee.property.value;
    //如果totalObj中有相应节点，就进行替换
    if (totalObj[objName] && totalObj[objName][propName]) {
      let myFunc = totalObj[objName][propName]; //Node中的代码为function (_0x32a55a, _0x4df6cd) {return _0x32a55a + _0x4df6cd;},
      //原始代码中，没有return
      let returnExpr = myFunc.body.body[0].argument;
      if (t.isBinaryExpression(returnExpr)) {
        let binExpr = t.binaryExpression(returnExpr.operator, path.node.arguments[0], path.node.arguments[1]);
        path.replaceWith(binExpr);
      } else if (t.isCallExpression(returnExpr)) {
        //function (_0x56e39c, _0x1a2cd7) {return _0x56e39c(_0x1a2cd7,_0x1a2cd7);},
        //这样式的,就拼装成callExpression
        let paramsArray = path.node.arguments.slice(1);
        let callExpr = t.callExpression(path.node.arguments[0], paramsArray);
        path.replaceWith(callExpr);
      }
    }
  }
});


//花指令还原后，可以删除原始代码中的ObjectExpression（先判断有没有引用，没有就删除）
traverse(ast, {
  VariableDeclarator(path) {
    if (t.isObjectExpression(path.node.init)) {
      path.remove();
    }
  }
})

let code = generator(ast).code;
fs.writeFile('./res3.js', code, (err) => {
});