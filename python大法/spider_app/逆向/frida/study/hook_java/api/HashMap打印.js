var utils = Java.use("com.xjb.hook.Utils");
var stringBUilder = Java.use("java.lang.StringBuilder");

utils.shufferMap.implementation = function (a) {
  //获取hashmap的所有值，模拟java遍历
  var key = a.keySet();
  var it = key.iterator();
  var res = stringBUilder.$new();//初始化
  while (it.hasNext) {
    var keyStr = it.next();
    var valuestr = a.get(keyStr);
    res.append(valuestr);
  }
}