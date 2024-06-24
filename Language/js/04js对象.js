/*
在 JavaScript 中，几乎“所有事物”都是对象。

布尔是对象（如果用 new 关键词定义）
数字是对象（如果用 new 关键词定义）
字符串是对象（如果用 new 关键词定义）
日期永远都是对象
算术永远都是对象
正则表达式永远都是对象
数组永远都是对象
函数永远都是对象
对象永远都是对象
*/
//可以类比Python中的字典
let a = {'a': 'tian'} //python中的浅拷贝，只是引用，不是值复制，值无序
let b = a;
b['a'] = 'c'
console.log(a);


//遍历
let person = {fname: "Bill", lname: "Gates", age: 62};
let txt=''
for (x in person) {
  console.log(x)
  txt += person[x];
}
person.name='tian' //添加属性
console.log(person)
delete person['name'] //删除属性
console.log(person)