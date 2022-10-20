var soAddr = Module.findBaseAddress("libxiaojianbang.so");
var funAddr = soAddr.add(0x124C);
var jStrtocstr = new NativeFunction(funAddr, 'pointer', ['pointer', 'pointer']);//创建函数指针
// var env = Java.vm.getEnv(); //get env
var env = Java.vm.tryGetEnv(); //try get env
console.log('env', JSON.stringify(env))
var jstring = env.newStringUtf("tmb"); //主动调用jni方法，构建参数
var res = jStrtocstr(env, jstring);
console.log('res', res.readCString())