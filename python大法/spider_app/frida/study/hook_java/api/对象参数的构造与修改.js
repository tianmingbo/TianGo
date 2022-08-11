var wallet = Java.user("com.xjb.hook.Wallet")
var money = Java.use("com.xjb.hook.Money");

wallet.deposit.implementation = function (a) {
  a.amount.value = 3000; //可修改属性的值
  console.log('wallet.deposit param:', a.getInfo())
  return this.deposit(money.$new("dollor", 200)) //构造参数
}