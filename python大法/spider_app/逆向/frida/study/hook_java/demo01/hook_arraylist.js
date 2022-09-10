Java.perform(function () {
  function showStacks() {
    //$new() 实例化一个对象
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use('java.lang.Throwable').$new()))
  }

  var arraylist = Java.use("java.util.ArrayList");
  arraylist.add.overload('java.lang.Object').implementation = function (a) {
    // if (a.equals("username")) {
      // showStacks();
      console.log("arraylist.add", a);
    // }
    return this.add(a);
  }
})

//frida -UF -l test.js