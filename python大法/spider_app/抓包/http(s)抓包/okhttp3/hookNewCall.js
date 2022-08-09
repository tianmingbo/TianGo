Java.perform(function () {
  var OkHttpClient = Java.use("okhttp3.OkHttpClient");

  OkHttpClient.newCall.implementation = function (request) {
    var res = this.newCall(request);
    console.log(request.toString())
    return res;
  }
})
