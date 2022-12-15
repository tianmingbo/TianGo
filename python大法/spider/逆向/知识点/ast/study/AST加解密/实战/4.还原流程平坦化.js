const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');

const jscode = fs.readFileSync("./res3.js", {
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

ast = generateObj(ast);

//避免因为嵌套的switch导致顺序错乱，一次只恢复switch流程平坦化
for (let i = 0; i < 20; i++) {
  traverse(ast, {
    MemberExpression(path) {
      //获取分发器
      if (t.isStringLiteral(path.node.object) &&
        t.isStringLiteral(path.node.property, {value: 'split'})) {
        //找到VariableDeclaration，和switch同一层级
        let varPath = path.findParent(function (p) {
          return t.isVariableDeclaration(p);
        })
        //获取下一个同层级节点
        let whilePath = varPath.getSibling(varPath.key + 1);
        //解析switch结构
        let myArr = [];
        whilePath.node.body.body[0].cases.map(function (p) {
          myArr[p.test.value] = p.consequent[0]; //key 和处理语句
        })

        //复原代码顺序
        let parentPath = whilePath.parent;
        varPath.remove();//删除代码
        whilePath.remove();
        let shuffleArr = path.node.object.value.split('|')
        // console.log(shuffleArr)
        shuffleArr.map(function (v) {
          parentPath.body.push(myArr[v]);
        });
        path.stop();
      }
    }
  })
}


let code = generator(ast).code;
fs.writeFile('./res4.js', code, (err) => {
});