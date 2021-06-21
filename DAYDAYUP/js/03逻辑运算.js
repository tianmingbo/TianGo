//逻辑运算
let age = 33
let voteable = (age < 18) ? "年轻" : "old"


//if |else if| else
let a = 1
if (a === 1) {
 console.log('a')
} else if (a===2) {

} else {
}

//switch
switch (new Date().getDay()) {
    case 0:
        day = "星期天";
        break;
    case 1:
        day = "星期一";
         break;
    case 2:
        day = "星期二";
         break;
    case 3:
        day = "星期三";
         break;
    case 4:
        day = "星期四";
         break;
    case 5:
        day = "星期五";
         break;
    case 6:
        day = "星期六";
}
// console.log(day)


//for in
let person = {fname:"Bill", lname:"Gates", age:62}; 

let text = "";
let x;
for (x in person) {
    text += person[x];
}
console.log(text)

//do while,至少会执行一次，因为判断在执行流程后
let i=0
do {
    text += "The number is " + i;
    i++;
 }
while (i < 10);

//正则表达式
let patt = /tian/i; // i：忽略大小写 g ：查询所有，而不是查询一个就停止
let str = "Tian MiNg";
let n = str.search(/ming/i); //search 返回匹配的index
/test/.test('test') // 返回布尔值
// /best/.exec("The bestst things in life are free!"); //返回匹配到的字符
console.log(n)
