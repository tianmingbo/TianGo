function print_arg(addr) {
    var module = Process.findRangeByAddress(addr);
    if (module != null) return hexdump(addr) + "\n";
    return ptr(addr) + "\n";
}

function hook_native_addr(funcPtr, paramsNum) {
    var module = Process.findModuleByAddress(funcPtr);
    Interceptor.attach(funcPtr, {
        onEnter: function (args) {
            this.logs = [];
            this.params = [];
            this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
            for (let i = 0; i < paramsNum; i++) {
                this.params.push(args[i]);
                this.logs.push("this.args" + i + " onEnter: " + print_arg(args[i]));
            }
        }, onLeave: function (retval) {
            for (let i = 0; i < paramsNum; i++) {
                this.logs.push("this.args" + i + " onLeave: " + print_arg(this.params[i]));
            }
            this.logs.push("retval onLeave: " + print_arg(retval) + "\n");
            console.log(this.logs);
        }
    });
}

Java.perform(function () {
    var Utils = Java.use("com.hoge.android.jni.Utils");
    Utils.signature.implementation = function (a, b) {
        //console.log("Utils.signature:", a, "||", b);
        var retval = this.signature(a, b);
        console.log(retval);
        return retval;
    }
});

function call_java() {
    Java.perform(function () {
        var Utils = Java.use("com.hoge.android.jni.Utils");
        Utils.$new().signature("4.0.0", "1632814143009d0rkV9");
    });
}

var soAddr = Module.findBaseAddress("libm2o_jni.so");
var sha1_encode = soAddr.add(0xA86C + 1);
//hook_native_addr(sha1_encode, 3);
Interceptor.attach(sha1_encode, {
    onEnter: function (args) {
        console.log(args[0].readCString());
        this.args2 = args[2];
    }, onLeave: function (retval) {
        console.log(hexdump(this.args2.readPointer())); //二级指针，需要再取下指针所指向的值
    }
});



