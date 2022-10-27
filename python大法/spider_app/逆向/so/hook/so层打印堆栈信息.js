//so层打印函数栈
console.log(Thread.backtrace(this.context, Backtracer.FUZZY).map(DebugSymbol.fromAddress).join('\n') + '\n');

var soAddr = Module.findBaseAddress("libxiaojianbang.so");
var updateAddr = soAddr.add(0x21B0);
Interceptor.attach(updateAddr, {
    onEnter: function (args) {
        //console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
        console.log("==================================================");
        console.log(soAddr);
        console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(function (value) {
            var symbol = DebugSymbol.fromAddress(value);
            console.log(symbol.moduleName);
            if (symbol.moduleName === "libxiaojianbang.so") {
                return symbol + " offset: " + value.sub(soAddr);
            }
            return symbol;
        }).join('\n'));
    }, onLeave: function (retval) {

    }
});
