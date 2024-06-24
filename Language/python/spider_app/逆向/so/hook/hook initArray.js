function main() {

    var dlopen = Module.findExportByName("libdl.so", "dlopen");
    var android_dlopen_ext = Module.findExportByName("libdl.so", "android_dlopen_ext");
    hook_dlopen(dlopen, "libxiaojianbang.so");
    hook_dlopen(android_dlopen_ext, "libxiaojianbang.so");
    var isHooked = false;

    function hook_dlopen(addr, soName, callback) {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                var soPath = args[0].readCString();
                if (soPath.indexOf(soName) !== -1) hook_call_constructors();
            }, onLeave: function (retval) {
            }
        });
    }

    function hook_call_constructors() {
        var symbols = Process.getModuleByName("linker64").enumerateSymbols();
        var call_constructors_addr = null;
        for (let i = 0; i < symbols.length; i++) {
            var symbol = symbols[i];
            if (symbol.name.indexOf("__dl__ZN6soinfo17call_constructorsEv") !== -1) {
                call_constructors_addr = symbol.address;
            }
        }
        console.log("call_constructors_addr: ", call_constructors_addr);
        Interceptor.attach(call_constructors_addr, {
            onEnter: function (args) {
                if (!isHooked) {
                    //函数只能replace一次，所以加上isHooked判断
                    hook_initarray();
                    isHooked = true;
                }
            }, onLeave: function (retval) {
            }
        });
    }

    function hook_initarray() {
        var xiaojianbangAddr = Module.findBaseAddress("libxiaojianbang.so");
        var func1_addr = xiaojianbangAddr.add(0x1C54);
        var func2_addr = xiaojianbangAddr.add(0x1C7C);
        var func3_addr = xiaojianbangAddr.add(0x1C2C);
        //替换函数
        Interceptor.replace(func1_addr, new NativeCallback(function () {
            console.log("func1 is replaced!!!");
        }, 'void', []));

        Interceptor.replace(func2_addr, new NativeCallback(function () {
            console.log("func2 is replaced!!!");
        }, 'void', []));

        Interceptor.replace(func3_addr, new NativeCallback(function () {
            console.log("func3 is replaced!!!");
        }, 'void', []));
    }
}

main();

