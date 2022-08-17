Java.perform(function () {
    var Utils = Java.use("com.xjb.hook.Utils");
    var strarr = Java.array("Ljava.lang.String;", ['tian', "is", "a", "good man"]); //frida api构造java arr
    var res = Utils.funName(strarr);
    console.log(res)
})

