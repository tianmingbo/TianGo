Java.perform(() => {
  let MainActivity = Java.use('com.germey.appbasic1.MainActivity');//获取类指针
  console.log('start hook');
  //改写MainActivity类中的getMessage方法
  MainActivity.getMessage.implementation = (arg1, arg2) => {
    send('start hook')
    return '6'
  }
})