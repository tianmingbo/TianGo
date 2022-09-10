var money = Java.use("com.xjb.hook.Money");
money.$init.implementation = function (a, b) {
  console.log("money.$init param:", a, b);
  return this.$init("dollor:", 2000)
}
//除了String的构造函数是StringFactory，其他都是$init