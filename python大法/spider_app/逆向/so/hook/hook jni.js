//hook libart 来hook jni相关函数
function hook_jni() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    var newStringUtf = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if(symbol.name.indexOf("CheckJNI") === -1 && symbol.name.indexOf("NewStringUTF") !== -1){
            console.log(symbol.name, symbol.address);
            newStringUtf = symbol.address;
        }
    }
    Interceptor.attach(newStringUtf, {
        onEnter: function (args) {
            console.log("newStringUtf args: ", args[1].readCString());
        }, onLeave: function (retval) {
            console.log("newStringUtf retval: ", retval);
        }
    });
}

function hook_jni2() {
    var envAddr = Java.vm.tryGetEnv().handle.readPointer();
    var funAddr = envAddr.add(48).readPointer();
    //console.log(Instruction.parse(funAddr).toString());
    Interceptor.attach(funAddr, {
        onEnter: function (args) {
            console.log("FindClass args: ", args[1].readCString());
        }, onLeave: function (retval) {
            console.log("FindClass retval: ", retval);
        }
    });
}