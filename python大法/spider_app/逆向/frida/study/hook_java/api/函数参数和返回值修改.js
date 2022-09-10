var money = Java.use("com.xjb.hook.Money");
var str=Java.use("java.lang.String");

money.getInfo.implementation=function(){
  var res=this.getInfo();
  console.log(res)
  return str.$new("chendali");//实例化一个字符串
}

money.setFlag.implementation = function(a){
  console.log("para:",a)
  return this.setFlag("chendali");
}