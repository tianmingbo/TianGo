Java.perform(function () {
    var arrayList = Java.use("java.util.ArrayList").$new();
    var interger = Java.use("java.lang.Integer"); //基本类型转换成包装类
    var boolean = Java.use("java.lang.Boolean");
    arrayList.add("tian");
    arrayList.add(interger.$new("666"));
    arrayList.add(boolean.$new(true));
})

