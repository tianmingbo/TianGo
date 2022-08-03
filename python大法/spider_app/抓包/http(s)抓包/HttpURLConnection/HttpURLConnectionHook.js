//Objection虽然可以能够hook一个类的全部函数，但是无法hook一个类的构造函数.
//android hooking watch class_method java.net.URL.$init --dump-retur n --dump-args --dump-backtrace
function main() {
  Java.perform(function () {
    var URL = Java.use("java.net.URL");
    URL.$init.overload("java.lang.String").implementation = function (urlStr) {
      console.log('**********', urlStr);
      return this.$init(urlStr);
    }
    URL.openConnection.overload().implementation = function () {
      var result = this.openConnection();
      //openConnection()这个函数的返回值是HttpURLConnection抽象类的具体实现类，可以通过$className获取类的类名： com.android.okhttp.internal.huc.HttpsURLConnectionImpl
      console.log('openConnection() resultType=>', result.$className);
      return result;
    }

    var HttpsURLConnectionImpl = Java.use("com.android.okhttp.internal.huc.HttpsURLConnectionImpl"); //hook具体实现类
    HttpsURLConnectionImpl.setRequestProperty.implementation = function (a, b) {
      console.log(a, b);
      return this.setRequestProperty(a, b);//hook后重新执行这个方法
    }
  })
}


setImmediate(main)