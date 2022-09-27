function hook_suspected_function(targetSo) {
    const funcs = ['0x152c', '0x16c4', '0x16fc', '0x1734', '0x177c', '0x187c', '0x18b4', '0x18f4', '0x193c', '0x1974', '0x19a8', '0x1b60', '0x1c5c', '0x1e04', '0x1ecc', '0x1f14', '0x1fb0', '0x1ff0', '0x21c4', '0x2380', '0x25ac', '0x25ec', '0x262c', '0x2854', '0x2a1c', '0x2a8c', '0x2d04', '0x4264', '0x4360', '0x449c'];
    for (var i in funcs) {
        let relativePtr = funcs[i];
        let funcPtr = targetSo.add(relativePtr);
        hook_native_addr(funcPtr);
    }
}

function main() {
    var targetSo = Module.findBaseAddress('libxiaojianbang.so');
    hook_suspected_function(targetSo);
}

setImmediate(main);

function print_arg(addr) {
    var module = Process.findRangeByAddress(addr);
    if (module != null) {
        return hexdump(addr) + "\n";
    } else {
        return ptr(addr) + "\n";
    }
}

function hook_native_addr(funcPtr) {
    var module = Process.findModuleByAddress(funcPtr);
    Interceptor.attach(funcPtr, {
        onEnter: function (args) {
            this.args0 = args[0];
            this.args1 = args[1];
            this.args2 = args[2];
            this.args3 = args[3];
            this.logs = [];
            this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
            this.logs.push("this.args0 onEnter: " + print_arg(this.args0));
            this.logs.push("this.args1 onEnter: " + print_arg(this.args1));
            this.logs.push("this.args2 onEnter: " + print_arg(this.args2));
            this.logs.push("this.args3 onEnter: " + print_arg(this.args3));

        }, onLeave: function (retval) {
            this.logs.push("this.args0 onLeave: " + print_arg(this.args0));
            this.logs.push("this.args1 onLeave: " + print_arg(this.args1));
            this.logs.push("this.args2 onLeave: " + print_arg(this.args2));
            this.logs.push("this.args3 onLeave: " + print_arg(this.args3));
            this.logs.push("retval onLeave: " + retval + "\n");
            console.log(this.logs);
        }
    });
}
