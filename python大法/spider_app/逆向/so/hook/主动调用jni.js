//主动调用jni函数
function call_jni() {
    //frida主动调用
    var retval = Java.vm.tryGetEnv().newStringUtf("xiaojianbang"); //创建字符串
    console.log(retval);
    console.log(Java.vm.tryGetEnv().getStringUtfChars(retval).readCString()); //输出结果
}

function call_jni2() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    var newStringUtf = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if (symbol.name.indexOf("CheckJNI") === -1 && symbol.name.indexOf("NewStringUTF") !== -1) {
            // console.log(symbol.name, symbol.address);
            newStringUtf = symbol.address;
        }
    }
    var newStringUtf_func = new NativeFunction(newStringUtf, 'pointer', ['pointer', 'pointer']);
    var jstring = newStringUtf_func(Java.vm.tryGetEnv().handle, Memory.allocUtf8String("xiaojianbang"));
    console.log(jstring);

    var envAddr = Java.vm.tryGetEnv().handle.readPointer();
    var GetStringUTFChars = envAddr.add(0x548).readPointer();
    var GetStringUTFChars_func = new NativeFunction(GetStringUTFChars, 'pointer', ['pointer', 'pointer', 'pointer']);
    var cstr = GetStringUTFChars_func(Java.vm.tryGetEnv().handle, jstring, ptr(0));
    console.log(cstr.readCString());

}