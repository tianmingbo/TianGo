//hook libc读写文件
function writeTxt() {
    var fopenAddr = Module.findExportByName('libc.so', 'fopen');
    var fputsAddr = Module.findExportByName('libc.so', 'fputs');
    var fcloseAddr = Module.findExportByName('libc.so', 'fclose');
    console.log(fopenAddr, fputsAddr, fcloseAddr);
    var fopen = new NativeFunction(fopenAddr, 'pointer', ['pointer', 'pointer']); //获取函数指针
    var fputs = new NativeFunction(fputsAddr, 'int', ['pointer', 'pointer']);
    var fclose = new NativeFunction(fcloseAddr, 'int', ['pointer']);
    var fileName = Memory.allocUtf8String("sdcard/tmp.txt"); //返回指针
    var text = Memory.allocUtf8String("tmb 66666");
    var mode = Memory.allocUtf8String('w'); //模式
    var file = fopen(fileName, mode);
    console.log(file);
    fputs(text, file);
    fclose(file);
}