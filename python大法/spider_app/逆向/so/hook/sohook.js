//枚举导入表
// var imports = Module.enumerateImports("libencryptlib.so");
// // console.log(JSON.stringify(imports[0]))
// for (let i = 0; i < imports.length; i++) {
//     console.log(imports[i].name + " " + imports[i].address);
// }
//
//枚举导出表
// var exports = Module.enumerateExports("libencryptlib.so");
// for (let i = 0; i < exports.length; i++) {
//     console.log(exports[i].name + " " + exports[i].address);
// }

//枚举符号表
// var symbols = Module.enumerateSymbols("libencryptlib.so");
// for (let i = 0; i < symbols.length; i++) {
//     console.log(symbols[i].name + " " + symbols[i].address);
// }

// 枚举进程中已加载的模块,同时也可以获得导出表
// var modules = Process.enumerateModules();
// console.log(JSON.stringify(modules[0].enumerateExports()[0]));


//导出函数的hook
// var funcAddr = Module.findExportByName("libencryptlib.so", "_ZN7MD5_CTX11MakePassMD5EPhjS0_");
// console.log(funcAddr);
//对funcAddr进行hook,首先执行onEnter里的方法,再执行onLeave的方法
// Interceptor.attach(funcAddr, {
//     onEnter: function (args) {
//         console.log("funcAddr onEnter args[1]: ", hexdump(args[1]));
//         console.log("funcAddr onEnter args[2]: ", args[2].toInt32()); //输出10进制
//         this.args3 = args[3];
//     }, onLeave: function (retval) {
//         console.log("funcAddr onLeave args[3]: ", hexdump(this.args3));
//     }
// });


//得到模块基址.当在导出表,符号表.导入表中不存在时,地址需要自己计算
//so基址+函数在so中的偏移[+1]
//1. 函数地址的计算
// 如果是thumb指令，函数地址计算方式：so基址 + 函数在so中的偏移 + 1
// 如果是arm指令，函数地址计算方式：so基址 + 函数在so中的偏移
// 2. 在安卓中，32位的so中的函数，基本都是thumb指令
// 3. 在安卓中，64位的so中的函数，基本都是arm指令
// var module1 = Process.findModuleByName("libencryptlib.so");
// // console.log(JSON.stringify(module1));
// console.log("module1", module1.base); //得到基址

// var module2 = Process.getModuleByName("libencryptlib.so");
// // console.log(JSON.stringify(module1));
// console.log("module2", module2.base); //得到基址

// var address = Module.findBaseAddress("libencryptlib.so");
// // console.log(JSON.stringify(module1));
// console.log("address:", address); //得到基址

// var modules = Process.enumerateModules(); //遍历moudle
// for (let i = 0; i < modules.length; i++) {
//     if (modules[i].name === "libencryptlib.so") {
//         console.log(modules[i].name + " " + modules[i].base);
//     }
// }

// var module = Process.findModuleByAddress(Module.findBaseAddress("libencryptlib.so"));
// console.log("module " + module.name + " " + module.base);


// hook任意函数,寻找地址
// var soAddr = Module.findBaseAddress("libencryptlib.so");
// // var so = 0x77ab999000;
// // console.log(ptr(so).add(0x1FA38)); // new NativePointer()
// var funcAddr = soAddr.add(0x1FA38);
// Interceptor.attach(funcAddr, {
//     onEnter: function (args) {
//         console.log("funcAddr onEnter args[1]: ", hexdump(args[1]));
//         console.log("funcAddr onEnter args[2]: ", args[2].toInt32());
//         this.args3 = args[3];
//     }, onLeave: function (retval) {
//         console.log("funcAddr onLeave args[3]: ", hexdump(this.args3));
//     }
// });


// 有手就行的so hook
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

var soAddr = Module.findBaseAddress("libencryptlib.so");
var funcAddr = soAddr.add(0x1FA38);
hook_native_addr(funcAddr, 4);