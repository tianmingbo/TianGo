Java.perform(function () {
  var OkHttpClient = Java.use("okhttp3.OkHttpClient");

  OkHttpClient.newCall.implementation = function (request) {
    var res = this.newCall(request);
    console.log(request.toString()) //只能hook request，不能hook response
    return res;
  }
})
