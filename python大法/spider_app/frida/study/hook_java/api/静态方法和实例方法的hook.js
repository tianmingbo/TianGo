//静态方法和实例方法的hook
//不需要区分修饰符,不需要区分静态和实例方法,hook代码写法一样

var money = Java.use("com.xjb.hook.Money");
//hook实例方法
money.getInfo.implementation = function () {
  var res = this.getInfo();
  console.log("money.getInfo res:", res);
  return res;
}
//hook静态方法
money.setFlag.implementation = function (a) {
  console.log("money.setFlag para:", a);
  return this.setFlag(a);
}