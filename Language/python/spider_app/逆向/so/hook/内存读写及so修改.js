// 内存读写
var soAddr = Module.findBaseAddress("libxiaojianbang.so");
// console.log(hexdump(soAddr.add(0x38A1)));
console.log(soAddr.add(0x38A1).read);
// console.log(soAddr.add(0x38A1).writeByteArray(stringToBytes("0123456789abcdef")));
// console.log(soAddr.add(0x38A1).readByteArray(33));
//
// var addr = Memory.alloc(13);
// addr.writeByteArray(stringToBytes("xiaojianbang\0"));
// console.log(addr.readByteArray(13));
// var str = Memory.allocUtf8String("xiaojianbang"); //申请内存，存入字符串
// console.log("Memory.allocUtf8String: ", str.readByteArray(13));
//Memory.protect(ptr(libso.base), libso.size, 'rwx'); //修改内存权限rwx

function modifyCode() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");

    // var codeAddr = soAddr.add(0x1684);
    // Memory.protect(codeAddr, 4, 'rwx');
    // codeAddr.writeByteArray(hexToBytes("0001094B"));  //sub w0, w8, w9 修改汇编代码
    // console.log(Instruction.parse(codeAddr).toString()); //输出汇编代码
    //
    // new Arm64Writer(soAddr.add(0x167C)).putNop(); //Nop跳过
    // console.log(Instruction.parse(soAddr.add(0x167C)).toString());

    var codeAddr = soAddr.add(0x1684); //执行到0x1684进入下方回调
    Memory.patchCode(codeAddr, 4, function (code) {
        var writer = new Arm64Writer(code, {pc: codeAddr});
        writer.putBytes(hexToBytes("0001094B"));  //sub w0, w8, w9
        writer.putBytes(hexToBytes("FF830091"));  //ADD SP, SP, #0x20
        writer.putRet();
        writer.flush();
    });

}

