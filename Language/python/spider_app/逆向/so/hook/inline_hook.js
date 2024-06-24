/*
* 汇编级别hook
* */
function inlineHook() {
    // var nativePointer = Module.findBaseAddress("libxiaojianbang.so");
    // var hookAddr = nativePointer.add(0x17BC); //汇编所在的地址
    // Interceptor.attach(hookAddr, {
    //     onEnter: function (args) {
    //         console.log("onEnter: ", this.context.x8.toInt32()); //输出寄存器内容
    //     }, onLeave: function (retval) {
    //         console.log("onLeave: ", this.context.x8.toInt32());
    //         // console.log(this.context.x8 & 7); //取后三位，与111位与
    //     }
    // });

    var nativePointer = Module.findBaseAddress("libxiaojianbang.so");
    var hookAddr = nativePointer.add(0x1B70);
    Interceptor.attach(hookAddr, {
        onEnter: function (args) {
            console.log("onEnter: ", this.context.x1);
            console.log("onEnter: ", hexdump(this.context.x1)); //如果是地址,直接hexdump
        }, onLeave: function (retval) {

        }
    });
}