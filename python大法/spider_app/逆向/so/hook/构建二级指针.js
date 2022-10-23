// 二级指针的构造
function call_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    var xiugaiStr = soAddr.add(0x17D0);//函数地址
    var xiugaiStr_func = new NativeFunction(xiugaiStr, 'int64', ['pointer']);
    var strAddr = Memory.allocUtf8String("dajianbang"); //一级指针
    console.log(hexdump(strAddr));
    var finalAddr = Memory.alloc(8).writePointer(strAddr);//构建二级指针
    xiugaiStr_func(finalAddr);
    console.log(hexdump(strAddr));
}