// // 引入 events 模块
// var events = require('events');
// // 创建 eventEmitter 对象
// var eventEmitter = new events.EventEmitter();
//
// // 创建事件处理程序
// var connectHandler = function connected() {
//     console.log('连接成功。');
//
//     // 触发 data_received 事件
//     eventEmitter.emit('data_received');//3
// }
//
// // 绑定 connection 事件处理程序
// eventEmitter.on('connection', connectHandler);//2
//
// // 使用匿名函数绑定 data_received 事件
// eventEmitter.on('data_received', function () {
//     console.log('数据接收成功。');//4
// });
//
// // 触发 connection 事件
// eventEmitter.emit('connection'); //1
//
// console.log("程序执行完毕。"); //5


//********************************************************************************************************************
// on 和 emit。on 函数用于绑定事件函数，emit 属性用于触发一个事件
var EventEmitter = require('events').EventEmitter;

var event = new EventEmitter();
event.on('some_event', function () {
    console.log("some_event is run");
});
setTimeout(function () {
    event.emit('some_event');
},1000);


//******************************************************************************************************************
