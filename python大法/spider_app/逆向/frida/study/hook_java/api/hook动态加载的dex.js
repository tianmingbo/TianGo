Java.perform(function () {
    //类可能是由不同的类加载器加载，当类时动态加载的时候可以使用这个尝试
    Java.enumerateClassLoaders({ //遍历所有类加载器
        onMatch: function (loader) {
            try {
                Java.classFactory.loader = loader;
                var dynamic = Java.use("com.xjb.app.Dynamic")
                console.log("dynamic", dynamic);
                dynamic.sayHello.implementation = function () {
                    console.log("hook dynamic.sayHello is run")
                    return "tian6"
                }
            } catch (e) {
                console.log(loader)
            }
        },
        onComplete: function () {
        }
    })
})

