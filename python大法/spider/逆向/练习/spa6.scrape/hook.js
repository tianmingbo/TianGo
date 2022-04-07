(function () {
  'use strict'

  function hook(object, attr) {
    let func = object[attr]; //func赋值
    object[attr] = function () {
      console.log('hooked', object, attr, arguments); //输出结果
      let ret = func.apply(object, arguments); //重新执行func
      debugger;
      console.log('ret', ret);
      return ret;
    }
  }

  hook(window, 'btoa') //hook base64加密
})()