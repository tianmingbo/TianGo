const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');

const jscode = fs.readFileSync("./res1.js", {
  encoding: "utf-8"
});


let ast = parser.parse(jscode);
var totalObj = {};

function generateObj(ast) {
  //解析原始代码中的ObjectExpression节点，
  /**
   * _0x1f20d3 = {
    'oscqj': "2|9|3|10|12|0|15|7|6|4|1|8|16|5|11|17|13|14|18",
    'fkUhC': "17|15|4|10|5|16|14|0|8|9|3|18|12|1|2|7|13|6|11",
   *
   * 上述结果为
   * {
   *   _0x1f20d3:{
   *     'oscqj':Node{},
   *     'fkUhC':Node{},
   *   },……
   * }
   * */
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
      ;
    }
  });
  return ast;
}

function findRealValue(node) {
  //ObjectProperty中有三种类型,以下处理MemberExpression类型
  if (t.isMemberExpression(node)) {
    let objName = node.object.name;
    let propertyName = node.property.value;
    if (totalObj[objName][propertyName]) {
      return findRealValue(totalObj[objName][propertyName]);
    } else {
      return false;
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
        let realNode = findRealValue(p.value);
        realNode && (p.value = realNode); //进行节点替换
      })
    }
  }
})

ast = generateObj(ast); //更新totalObj对象

traverse(ast, {
  MemberExpression(path) {
    let objName = path.node.object.name;
    let propName = path.node.property.value;
    totalObj[objName] && t.isStringLiteral(totalObj[objName][propName]) && path.replaceWith(
      totalObj[objName][propName]
    )
  }
});

let code = generator(ast).code;
fs.writeFile('./res2.js', code, (err) => {
});