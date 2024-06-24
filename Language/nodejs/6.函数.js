function execute(someFunction, value) {
    someFunction(value);
}

//传递匿名函数
execute(function (word) {
    console.log(word);
}, "Hello");

function say(word) {
    console.log('hello ' + word);
}

//传递函数名
execute(say, 'tmb')