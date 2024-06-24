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


//修改函数数值参数和返回值
var soAddr = Module.findBaseAddress("libxiaojianbang.so");
console.log("soAddr", soAddr);
var add = soAddr.add(0x165C);
Interceptor.attach(add, {
    onEnter: function (args) {
        args[2] = ptr(1000); // new NativePointer
        console.log(args[2].toInt32());
        console.log(args[3]);
        console.log(args[4]);
    }, onLeave: function (retval) {
        retval.replace(1000);  //修改返回值
        console.log(retval.toInt32());
    }
});