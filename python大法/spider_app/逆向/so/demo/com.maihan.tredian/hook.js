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
    var TreUtil = Java.use("com.maihan.tredian.util.TreUtil");
    TreUtil.sign.implementation = function (args) {
        console.log("TreUtil.signStr:", args);
        var retval = this.sign(args);
        console.log(retval);
        return retval;
    }
});

function call_java(){
    Java.perform(function () {
        var TreUtil = Java.use("com.maihan.tredian.util.TreUtil");
        TreUtil.sign("app_ver=100&nonce=wi3nwo1632749058036&timestamp=1632749058&tzrd=BwzXzSGFyiPstMIVuzTZb7LzTZzbXRJOFzpbQiIaT7tLD0cc1eFFficAAUFoQPlbwk1GAlvWKaP4ipqRnbsFguJ0fALWPNMT6vcqr2uBwiETYt29YHmXhn+VadBnDGFnvzttJTttfKExb/bBJFSuEHKUKh+upPAGYjMNZN9hK1OdN9HxyH8Nx5BM2BnciDsQzjZLg8JAmGuHYiIUedIZaiRuUL/1np58iIU3duQ3B4KPTXvpPYb97T0ARzf8TjQp//LpfYv+QBaqNu6CBaKolV77fC1pqaR7v6eai7CIAABbWAKj6xanD+GEEDzvSTz7ZxTiZrCnAf9+0dNq7QfzbI/uf9LhD+24MshM4pcKh6FpA1PwcHH9wFWofI8dw8KCcrMdLfQ4303sA4Bp/ghN9IzBBtMIj21UAcFFgkch1iKcVTbJ8dlNWk679L7bHDutTmKSZ556wvrhtklUg9yDi0KKS/3QiNVcTXfXj+N/3T4=");
    });
}

//hook sign参数
var soAddr = Module.findBaseAddress("libtre.so");
// var SHA1Result = soAddr.add(0x14C8 + 1);
// hook_native_addr(SHA1Result, 2);

// var SHA1Input = soAddr.add(0x15BE + 1);
// //hook_native_addr(SHA1Input, 3);
// Interceptor.attach(SHA1Input, {
//    onEnter: function (args) {
//        //console.log(args[1].readCString());
//        console.log(hexdump(args[1], {
//            offset: 0,
//            length: args[2].toInt32(),   //这里只能接收十进制的
//            header: true,
//            ansi: false
//        }));
//    }, onLeave: function (retval) {
//
//     }
// });

//
var base64_encode_new = soAddr.add(0x13B4 + 1);
// hook_native_addr(base64_encode_new, 3);
Interceptor.attach(base64_encode_new, {
   onEnter: function (args) {
       console.log(args[0].readCString());
       this.args1 = args[1];
   }, onLeave: function (retval) {
        console.log(this.args1.readCString());
    }
});
