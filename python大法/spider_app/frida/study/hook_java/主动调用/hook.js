function main() {
  console.log('script loaded successfully')
  Java.perform(function () {
    console.log('Inside java perform')
    var MainActivity = Java.use('com.xjb.demo02.MainActivity');//hook 函数所在的类名
    MainActivity.staticSecret();//调用类方法是直接调用
    //对象方法主动调用
    /*
    * 如果想要主动调用对象方法，就需要存在相应类的对象，否则就无法进入choose逻辑。
    * 因为app打开就运行在MainActivity页面，所以必然存在MainActivity类对象。
    * */
    Java.choose('com.xjb.demo02.MainActivity', {
      onMatch: function (instance) {
        console.log('instance found', instance);
        instance.secret();
      },
      onComplete: function () {
        console.log('search complete');
      }
    })
  })
}

setImmediate(main)//当frida注入app后立即执行main函数