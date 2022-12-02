const fs = require('fs');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;
const t = require('@babel/types');
const traverse = require('@babel/traverse').default;

const jsCode = 'let obj = {\n' +
  '  name: "\u9648\u5927\u529b",\n' +
  '  add: function (a, b) {\n' +
  '    return a + b + 100;\n' +
  '  },\n' +
  '  mul: function (a, b) {\n' +
  '    return a * b + 10000;\n' +
  '  }\n' +
  '}'

let ast = parser.parse(jsCode);
const updateNode = {
  Identifier(path) {
    if (path.node.name === this.paramName) {
      path.node.name = "x";
    }
    // console.log(path);
    path.stop(); //停止遍历
  }, ReturnStatement(path) {
    path.replaceWithMultiple([t.returnStatement()]);
    path.replaceWithSourceString("x+b+1000") //源码替换
    path.stop();
  }

}


const visitor = {
  FunctionExpression(path) {
    const paramName = path.node.params[0].name;

    //节点是path中的一部分，path是一个对象，用来描述两个节点间的连接
    path.traverse(updateNode, {paramName})
  },
  BinaryExpression(path) {
    console.log(path.get('right').isNumericLiteral()) //判断path类型
    path.node.left = t.identifier("x"); //替换节点属性
    path.node.right = t.identifier("b");
    // path.replaceWith(t.stringLiteral("chendali"));//替换整个节点
  },
  EmptyStatement(path) {
    path.remove();//删除节点
  },
  ReturnStatement(path) {
    console.log(path.listKey) //容器名
    console.log(path.key) //容器索引
    console.log(path.container) //容器
    console.log(path.getSibling(path.key + 1)) //获取同级容器

  }
}

traverse(ast, visitor)

let code = generator(ast).code;
fs.writeFile('./demoNew.js', code, (err) => {
});