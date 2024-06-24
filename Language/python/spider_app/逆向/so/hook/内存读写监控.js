function hook_dlopen(addr, soName, callback) {
    Interceptor.attach(addr, {
        onEnter: function (args) {
            var soPath = args[0].readCString();
            if (soPath.indexOf(soName) != -1) this.hook = true;
        }, onLeave: function (retval) {
            if (this.hook) {
                callback()
            }
        }
    });
}

var dlopen = Module.findExportByName("libdl.so", "dlopen");
var android_dlopen_ext = Module.findExportByName("libdl.so", "android_dlopen_ext");
hook_dlopen(dlopen, "libxiaojianbang.so", set_read_write_break);
hook_dlopen(android_dlopen_ext, "libxiaojianbang.so", set_read_write_break);


function set_read_write_break() {

    Process.setExceptionHandler(function (details) {
        console.log(JSON.stringify(details, null, 2));
        console.log("lr", DebugSymbol.fromAddress(details.context.lr));
        console.log("pc", DebugSymbol.fromAddress(details.context.pc));
        Memory.protect(details.memory.address, Process.pointerSize, 'rwx');
        console.log(Thread.backtrace(details.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
        return true;
    });
    var addr = Module.findBaseAddress("libxiaojianbang.so").add(0x3CFD);
    Memory.protect(addr, 8, '---'); //修改内存页的权限

}


