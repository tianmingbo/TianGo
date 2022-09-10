rpc.exports = {
  sub: function CallSub(a, b) {
    Java.perform(function () {
      var Arith = Java.use('com.example.junior.util.Arith')
      var JavaString = Java.use('java.lang.String')
      //sub是静态方法，获取类对象即可完成函数的主动调用。
      //如果是实例函数,则首先需要创建实例,再完成函数调用
      var result = Arith.sub(JavaString.$new(a), JavaString.$new(b))
      console.log(a, "-", b, "=", result) // 最终修改为
      send(a, "-", b, "=", result)
    })

  }
}