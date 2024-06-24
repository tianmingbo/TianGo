var fs = require("fs");


//异步执行
fs.readFile('test.txt', function (err, data) {
    if (err) return console.error(err);
    console.log(data.toString());
})
console.log("程序结束！")