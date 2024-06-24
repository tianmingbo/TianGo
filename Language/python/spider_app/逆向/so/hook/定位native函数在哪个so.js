//获取静态注册在哪个so
function hook_dlsym() {
    var dlsymAddr = Module.findExportByName("libdl.so", "dlsym");
    console.log(dlsymAddr);
    Interceptor.attach(dlsymAddr, {
        onEnter: function (args) {
            this.args1 = args[1]; //参数1就是native函数名
        }, onLeave: function (retval) {
            var module = Process.findModuleByAddress(retval); //获取so信息
            if (module == null) return;
            console.log(this.args1.readCString(), module.name, retval, retval.sub(module.base)); //retval.sub(module.base) 获取函数偏移
        }
    });
}

// hook_dlsym();

//hook jni函数动态注册
function hook_RegisterNatives() {
    var symbols = Process.getModuleByName("libart.so").enumerateSymbols();
    var RegisterNatives_addr = null;
    for (let i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if (symbol.name.indexOf("CheckJNI") === -1 && symbol.name.indexOf("RegisterNatives") !== -1) {
            RegisterNatives_addr = symbol.address;
        }
    }
    console.log("RegisterNatives_addr: ", RegisterNatives_addr);

    Interceptor.attach(RegisterNatives_addr, {
        onEnter: function (args) {

            var env = Java.vm.tryGetEnv(); //env
            var className = env.getClassName(args[1]); //获取类名
            var methodCount = args[3].toInt32();  //获取方法数量

            for (let i = 0; i < methodCount; i++) {
                //args[2]结构体起始地址,Process.pointerSize->指针长度
                var methodName = args[2].add(Process.pointerSize * 3 * i).readPointer().readCString(); //readPointer() 获取指针指向的内容
                var signature = args[2].add(Process.pointerSize * 3 * i).add(Process.pointerSize).readPointer().readCString();
                var fnPtr = args[2].add(Process.pointerSize * 3 * i).add(Process.pointerSize * 2).readPointer();
                var module = Process.findModuleByAddress(fnPtr);
                console.log(className, methodName, signature, fnPtr, module.name, fnPtr.sub(module.base));
            }

        }, onLeave: function (retval) {
        }
    });


}

hook_RegisterNatives();
