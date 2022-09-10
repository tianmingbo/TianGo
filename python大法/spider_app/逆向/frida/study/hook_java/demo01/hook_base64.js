Java.perform(function () {
  function showStacks() {
    //$new() 实例化一个对象
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use('java.lang.Throwable').$new()))
  }

  var base64 = Java.use("android.util.Base64");
  base64.encodeToString.overload('[B', 'int').implementation = function (a, b) {
    showStacks();
    console.log("base64.encodeToString:", JSON.stringify(a));
    var res = this.encodeToString(a, b);
    console.log('res:', res);
    return res;
  }
})

//frida -UF -l test.js