Java.perform(function () {
  function showStacks() {
    //$new() 实例化一个对象
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use('java.lang.Throwable').$new()))
  }

  var hashMap = Java.use("java.util.HashMap");
  hashMap.put.implementation = function (a, b) {
    if (a.equals("username")) {
      showStacks();
      console.log("hashMap.put", a, b);
    }
    return this.put(a, b);
  }
})

//frida -UF -l test.js