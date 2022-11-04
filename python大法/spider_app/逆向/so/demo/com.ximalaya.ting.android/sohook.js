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

//ollvm加密解决
var soAddr = Module.findBaseAddress("liblogin_encrypt.so");
console.log(hexdump(soAddr.add(0xD060))); //直接读取对应内存地址的数据