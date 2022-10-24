//hook_dlopen
function hook_dlopen(addr, soName, callback) {
    Interceptor.attach(addr, {
        onEnter: function (args) {
            var soPath = args[0].readCString();
            if (soPath.indexOf(soName) != -1) this.hook = true;
        }, onLeave: function (retval) {
            if (this.hook) callback();
        }
    });
}

var dlopen = Module.findExportByName("libdl.so", "dlopen");
var android_dlopen_ext = Module.findExportByName("libdl.so", "android_dlopen_ext");
//console.log(JSON.stringify(Process.getModuleByAddress(dlopen)));
//hook_dlopen(dlopen, "libxiaojianbang.so", hook_JNIOnload);
//hook_dlopen(android_dlopen_ext, "libxiaojianbang.so", hook_JNIOnload);

function hook_JNIOnload() {
    var xiaojianbangAddr = Module.findBaseAddress("libxiaojianbang.so");
    var funcAddr = xiaojianbangAddr.add(0x1CCC);
    Interceptor.replace(funcAddr, new NativeCallback(function () {
        console.log("this func is replaced !");
    }, 'void', []));
}


