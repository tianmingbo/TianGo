function main() {
  Java.perform(function () {
    var Airth = Java.use('com.example.junior.util.Arith');
    Airth.sub.overload('java.lang.String', 'java.lang.String').implementation = function (str, str2) {
      var javaString = Java.use('java.lang.String');
      var res = this.sub(str, javaString.$new('123'));
      console.log(str, str2, res);
      console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new())) //打印调用栈
      return res;
    }
  })
}

setImmediate(main)