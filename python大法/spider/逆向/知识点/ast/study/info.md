## tool

1. https://astexplorer.net/  AST 解析
2. https://juejin.cn/post/6875970383447588871#heading-22 节点含义

## type

1. MemberExpression 成员表达式 console['log'] 或console.log
2. Identifier 标识符 如变量名，函数名，属性名，都归为标识符
3. ObjectExpression 对象表达式
4. VariableDeclaration 变量声明语句 var
5. StringLiteral 字符串字面量 'tian'
6. FunctionExpression 函数表达式
7. ReturnStatement 返回语句 return
8. BinaryExpression 二项式 1+2
9. NumericLiteral 数值字面量 1
10. Literal 字面量（本身语义就代表一个值的字面量）
11. RegExpLiteral 正则字面量
12. Programs 根节点 代表了一个完整的程序
13. FunctionDeclaration 函数声明 function
14. AssignmentExpression 赋值表达式 a=100
15. VariableDeclarator 变量声明符 var arr 声明变量arr
16. ArrayExpression 数组表达式 [1,2]
17. CallExpression 调用表达式 atob()
18. ExpressionStatement 表达式语句 a=a+1
19. BlockStatement 块语句