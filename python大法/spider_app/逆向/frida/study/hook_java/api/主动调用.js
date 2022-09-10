//主动调用，静态方法可以直接调用
//实例方法需要实例化一个对象才能调用,也可以搜索类中已存在的对象

Java.perform(function () {
  Java.choose("com.xjb.hook.Money", {
    onMatch: function (obj) {
      console.log(obj.getInfo());
    },
    onComplete: function () {
      console.log('内存中的Money对象搜索完毕！')
    }
  })
})

//android Context获取
var current_application = Java.use('android.app.ActivityThread').currentApplication();
var context = current_application.getApplicationContext();