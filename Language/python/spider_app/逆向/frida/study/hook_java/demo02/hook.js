function main() {
  console.log('script loaded successfully')
  Java.perform(function () {
    console.log('Inside java perform')
    var MainActivity = Java.use('com.xjb.demo02.MainActivity');//hook 函数所在的类名
    console.log('Java.use.Successfully')
    //对方法重载要做判断
    MainActivity.fun.overload('int', 'int').implementation = function (x, y) {
      console.log('x:', x, "y:", y);
      var ret_value = this.fun(x, 2);
      return ret_value;
    }
    MainActivity.fun.overload('java.lang.String').implementation = function (x) {
      console.log('x:', x);
      var ret_value = this.fun('tmp');
      return ret_value;
    }
  })
}

setImmediate(main)//当frida注入app后立即执行main函数