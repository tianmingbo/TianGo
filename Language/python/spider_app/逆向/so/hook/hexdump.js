var soAddr = Module.findBaseAddress("libxiaojianbang.so");
var updateAddr = soAddr.add(0x21B0);
Interceptor.attach(updateAddr, {
    onEnter: function (args) {
        //console.log(hexdump(args[1], {offset: 6, length: args[2].toUInt32(), header: false}));
        console.log(hexdump(args[1], {length: args[2].toUInt32(), header: false})); //length为整数
        console.log("==========================");

    }, onLeave: function (retval) {

    }
});




