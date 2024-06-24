//字符串方法
let a = "tian"
a.length //长度
a.indexOf('c', 2) //字符串中的位置,从第二个开始
let str = "Apple, Banana, Mango";
let res = str.slice(7, 13);//提取字符串，可以使用负值
str.substring(7, 13) //类似slice，不过不可以使用负值
str.substr(7, 6) //第二个参数时截取的长度
str.replace('Apple', 'tian') //替换字符串
str.toUpperCase() //转换为大写
str.toLowerCase() //转换为小写
str.concat(" ", "ss") //字符串连接，可以使用+连接
str.trim() //删除字符串两边的空格
str.charAt(0) //提取位于0位置的字符串
str.charCodeAt(0) //返回0位置的Unicode编码
str.split("") //分割为数组

//****************************数值方法
let x = 123;
x.toString()
x = 123.456
x.toFixed(2) //返回字符串值，保留两位
Number(new Date());//返回时间戳
parseInt('10 years') //返回第一个数值，没有返回NaN


//************************数组方法
let num = [1, 2, 3, 45, 6]
let num2 = [7, 8, 9]
num.toString() //转换为字符串'1，2，3，45，6'
num.join("") //合并字符串
num.pop() //删除最后一个元素
num.push('last') //追加元素
num.shift() //返回第一个元素，并删除第一个元素
num.unshift(0) //在数组首位添加元素，返回新数组的长度
delete num[0] //删除第一个元素
num2.concat(num) //数组合并
num.slice(1, 3) //下标1，2，不包括3
num.sort() //以字母序排序，不适合数组整数排序
num.sort(function (a, b) {
  return b - a
}); //对数字进行排序
num.reverse() //数组反转

function myArrayMax(arr) {
  //查找数组中的最小值
  return Math.max.apply(null, arr);
}

//数组遍历
num.forEach(function (data, index, array) {
  //data每个元素，index索引，array所有元素
  // console.log(data,index,array)
})
num.indexOf(1) //1的索引下标
num.lastIndexOf(1) //最后一个1的索引下标


//*******日期函数*****
let d = new Date();
console.log(d)

