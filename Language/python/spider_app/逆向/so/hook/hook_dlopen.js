/*
* 加载so的时候会使用dlopen
* 1. 有些函数在so首次加载的时候执行，而so没加载之前又不能去hook
2. 那么要hook这些函数，就必须监控so何时被加载
3. 因此，需要hook dlopen等系统函数，当so加载完毕，立刻hook
* */

function hook_dlopen(addr, soName, callback) {
    Interceptor.attach(addr, {
        onEnter: function (args) {
            var name = args[0].readCString();
            if (name.indexOf(soName) != -1) this.hook = true;
        }, onLeave: function (retval) {
            if (this.hook) callback();
        }
    });
}

function hook_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    console.log("soAddr", soAddr);
    var MD5Final = soAddr.add(0x3540);
    Interceptor.attach(MD5Final, {
        onEnter: function (args) {
            this.args1 = args[1];
        }, onLeave: function (retval) {
            console.log(hexdump(this.args1));
        }
    });
}

// var dlopen = Module.findExportByName(null, "dlopen"); //7.0以下api
var dlopen = Module.findExportByName("libdl.so", "dlopen"); //7.0以下api
var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");
hook_dlopen(dlopen, "libxiaojianbang.so", hookfunc);
hook_dlopen(android_dlopen_ext, "libxiaojianbang.so", hookfunc);
