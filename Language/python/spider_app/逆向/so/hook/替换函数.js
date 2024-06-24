//函数替换
var soAddr = Module.findBaseAddress("libxiaojianbang.so");
var addAddr = soAddr.add(0x1A0C);
Interceptor.replace(addAddr, new NativeCallback(function () {
    console.log(100);
}, 'void', []));
//
var add = new NativeFunction(addAddr, 'int', ['pointer', 'pointer', 'int', 'int', 'int']);
Interceptor.replace(addAddr, new NativeCallback(function (a, b, c, d, e) {
    console.log(a, b, c, d, e);
    var oldResult = add(a, b, c, d, e);
    console.log(oldResult);
    return 100;
}, 'int', ['pointer', 'pointer', 'int', 'int', 'int']));
//
var md5Addr = soAddr.add(0x1E3C);
Interceptor.replace(md5Addr, new NativeCallback(function () {
    return 100;
}, 'int', []));