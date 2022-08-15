Java.perform(function () {
    console.log(Java.enumerateClassLoadersSync().join('\n')); //枚举内存中的所有类

    //枚举类的所有方法
    var wallet = Java.use("com.xjb.hook.Wallet");
    var methods = wallet.class.getDeclaredMethods(); //通过反射的方法获取方法名，return array
    var constructors = wallet.class.getDeclaredConstructors(); //获取构造方法
    var fields = wallet.class.getDeclaredFields();//获取字段
    var classes = wallet.class.getDeclaredClasses();//获取内部类


    for (let i = 0; i < methods.length; i++) {
        console.log(methods[i].getName())
    }
})