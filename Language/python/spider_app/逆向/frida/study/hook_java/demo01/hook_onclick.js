Java.perform(function () {
  function showStacks() {
    //$new() 实例化一个对象
    console.log(Java.use("android.util.Log").getStackTraceString(Java.use('java.lang.Throwable').$new()))
  }

  var btn_login_id = Java.use("com.dodonew.online.R$id").btn_login.value;
  console.log('btn_login_id', btn_login_id);
  var view = Java.use("android.view.View");
  view.setOnclickListenter.implementation = function (a) {
    if (this.getId() == btn_login_id) {
      showStacks();
      console.log("view.id:", this.getId());
    }
    return this.setOnclickListenter(a);
  }
})
