Java.perform(function () {
    var classes = Java.enumerateLoadedClassesSync(); //获取已加载的类
    for (const index in classes) {
        let className = classes[index];
        if (className.indexOf('com.xjb') === -1) continue;
        let clazz = Java.use(className);
        let resArr = clazz.class.getInterfaces();//利用反射获取类的接口类
        if (resArr.length === 0) continue;
        for (let i = 0; i < resArr.length; i++) {
            if (resArr[i].toString().indexOf('com.xjb.app.textClassName') !== -1) {
                console.log(className, resArr[i]);
            }
        }
    }
})