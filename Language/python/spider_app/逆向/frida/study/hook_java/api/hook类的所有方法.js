//hook类的所有方法
Java.perform(function () {
    function hookFunc(methodName) {
        console.log(methodName);
        var overloadsArr = utils[methodName].overloads; //获取所有重载
        for (let j = 0; j < overloadsArr.length; j++) {
            overloadsArr[j].implementation = function () {
                var params = "";
                for (let k = 0; k < arguments.length; k++) {
                    params += arguments[k] + " ";
                }
                console.log("utils." + methodName + "is called! param is: ", params);
                return this[methodName].apply(this, arguments);
            }
        }
    }

    var utils = Java.use("com.xjb.hook.Utils");
    var methods = wallet.class.getDeclaredMethods(); //通过反射的方法获取方法名，return array
    for (let i = 0; i < methods.length; i++) {
        var methodName = methods[i].getName();
        hookFunc(methodName)
        console.log(methods[i].getName())
    }
})