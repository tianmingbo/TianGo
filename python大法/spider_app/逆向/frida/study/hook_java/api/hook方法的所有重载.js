Java.perform(function () {
  var utils = Java.use("com.xjb.hook.Utils");
  var overloadArr = utils.getCalc.overloads; //获取所有重载方法
  for (var i = 0; i < overloadArr.length; i++) {
    overloadArr[i].implementation = function () {
      var params = "";
      for (var j = 0; j < arguments.length; j++) {
        params += arguments[j] + " ";
      }
      console.log(params)
      return this.getCalc.apply(this, arguments); //返回值，apply接收两个参数，第一个是个对象，第二个是个数组
    }
  }
})