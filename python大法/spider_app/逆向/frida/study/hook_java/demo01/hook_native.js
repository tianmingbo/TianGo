Java.perform(function () {
  /*要hook native层，使用Interceptor.attach，
  * 有两个参数，第一个是指向Native方法的指针，第二个是Hook逻辑的实现*/
  Interceptor.attach(Module.findExportByName('libnative.so',
    'Java_com_germey_appbasic2_MainActivity_getMessage'), {
    onEnter: function (args) {
      //hook前执行的逻辑
      send('hook onEnter')
      send('args[1]=' + args[2])
      send('args[2]=' + args[3])
    },
    onLeave: function (val) {
      //之后执行的逻辑
      send('hook onLeave')
      val.replace(Java.vm.getEnv().newStringUtf('5'))
    }
  })
})

// Java.perform(function () {
//   var soaddr=Module
// })