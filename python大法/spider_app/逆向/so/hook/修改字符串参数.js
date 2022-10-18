/*
* 修改字符串参数
* 1. 把char*指向的字符串修改掉，新字符串一般不超出原字符串长度（一般不用，超出长度会引起错误）
2. 把so中已有的字符串地址传给函数（无法自定义字符串）
3. 修改MD5_CTX结构体中存放数据的内容
4. 构建新的字符串，需要注意构建的字符串变量的作用域（常用）
5. 替换函数
* */

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


function stringToBytes(str) {
    return hexToBytes(stringToHex(str));
}

// Convert a ASCII string to a hex string
function stringToHex(str) {
    return str.split("").map(function (c) {
        return ("0" + c.charCodeAt(0).toString(16)).slice(-2);
    }).join("");
}

function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;
}

// Convert a hex string to a ASCII string
function hexToString(hexStr) {
    var hex = hexStr.toString();//force conversion
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

// 修改函数字符串参数
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Update = soAddr.add(0x1D68);
// Interceptor.attach(MD5Update, {
//     onEnter: function (args) {
//         if(args[1].readCString() === "xiaojianbang"){
//             var newStr = "xiaojian";
//             args[1].writeByteArray(hexToBytes(stringToHex(newStr) + "00")); //字符串结尾加00
//             console.log(hexdump(args[1]));
//             args[2] = ptr(newStr.length);
//             console.log(args[2].toInt32());
//         }
//     }, onLeave: function (retval) {
//
//     }
// });

// frida操作C语言结构体
// var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log("soAddr", soAddr);
// var MD5Update = soAddr.add(0x1D68);
// Interceptor.attach(MD5Update, {
//     onEnter: function (args) {
//         this.args0 = args[0]; //结构体
//         // console.log(hexdump(args[0]));//读取结构体数据
//         this.args1 = args[1];
//         // if(args[1].readCString() == "xiaojianbang"){
//         //     args[1] = soAddr.add(0x38A1);
//         //     console.log(hexdump(args[1]));
//         //     args[2] = ptr(soAddr.add(0x38A1).readCString().length); //长度,数值参数加指针ptr()
//         //     console.log(args[2].toInt32());
//         // }
//     }, onLeave: function (retval) {
//         if (this.args1.readCString() === "xiaojianbang") {
//             console.log(hexdump(this.args0.add(24).writeByteArray(stringToBytes("dadajianbang")))); //修改结构体数据，24是偏移量
//             console.log('-------------------------------------------',hexdump(this.args0))
//         }
//     }
// });


//frida构建新的字符串，申请内存，创建字符串，注意js作用域
var soAddr = Module.findBaseAddress("libxiaojianbang.so");
console.log("soAddr", soAddr);
var MD5Update = soAddr.add(0x1D68);
var newStr = "gdfgdhfgjghjgkhjkh;kl;k;";
var newStrAddr = Memory.allocUtf8String(newStr); //生成新的字符串
Interceptor.attach(MD5Update, {
    onEnter: function (args) {
        this.args0 = args[0];
        this.args1 = args[1];
        if (args[1].readCString() === "xiaojianbang") {
            // var newStrAddr = Memory.allocUtf8String(newStr); //生成新的字符串,放在这里面,会出错,因为在onEnter结束后,内存被回收,this.newStrAddr即可，或定义成全局变量
            args[1] = newStrAddr;
            console.log(hexdump(args[1]));
            args[2] = ptr(newStr.length);
            console.log(args[2].toInt32());
        }
    }, onLeave: function (retval) {
        if (this.args1.readCString() === "xiaojianbang") {
            console.log(hexdump(this.args0));
        }
    }
});
