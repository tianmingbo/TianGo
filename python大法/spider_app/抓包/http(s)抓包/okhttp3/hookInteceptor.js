function hook_okhttp3() {
    Java.perform(function () {
        Java.openClassFile('/data/local/tmp/okhttp3logging.dex').load();//首先推送到对应目录，然后加载dex
        var myInterceptor = Java.use("com.xjb.http3demo.LoggingInterceptor");
        var objInterceptor = myInterceptor.$new(); //创建拦截器对象
        //利用建造者模式在Interceptor链中添加自定义拦截器
        var Builder = Java.use("okhttp3.OkHttpClient$Builder");
        console.log(Builder);
        Builder.build.implementation = function () {
            this.networkInterceptors().add(objInterceptor);
            return this.build();
        }

    })
}

function main() {
    hook_okhttp3();
}

setImmediate(main)
//需要使用spawn模式， 因为App全局只有一个client
//frida -U -f com.xjb.http3demo -l hookInteceptor.js --no-pause