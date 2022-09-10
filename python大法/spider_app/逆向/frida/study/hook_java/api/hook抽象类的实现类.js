Java.perform(function () {
    var classes = Java.enumerateLoadedClassesSync(); //获取已加载的类
    for (const index in classes) {
        let className = classes[index];
        if (className.indexOf('com.xjb') === -1) continue;
        let clazz = Java.use(className);
        let resClass = clazz.class.getSuperclass();//利用反射获取类的父类
        if (resClass.length == null) continue;
        //不需要遍历，因为只有一个父类
        if (resClass.toString().indexOf('com.xjb.app.textClassName') !== -1) {
            console.log(className, resClass);
        }
    }
})