package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import com.sun.jna.Pointer;

import java.io.*;

public class MonitorMemory extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;
    Pointer md5_ctx;

    MonitorMemory(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机

        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dmA = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbangA.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbang.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        module = dm.getModule(); // 加载好的 libxiaojianbang.so 对应为一个模块

        String traceFile = "yourpath";
        PrintStream traceStream = null;
        try {
            traceStream = new PrintStream(new FileOutputStream(traceFile), true);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        /*
        监控内存读写
         * 每条读写，unidbg提供这些信息
         * 写的位置、写了几个字节、写入什么值、发生写操作的地址、lr的值(程序的返回地址)
         * */
//        emulator.traceRead(module.base, module.base + module.size).setRedirect(traceStream); //监控整个so，输出重定向到文件流
//        emulator.traceWrite(module.base, module.base + module.size).setRedirect(traceStream);
        //trace 每行执行过的汇编
        emulator.traceCode(module.base, module.base + module.size).setRedirect(traceStream);
        System.out.println(Long.toHexString(module.base));

        dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        NativeHelper = vm.resolveClass("com/xiaojianbang/ndk/NativeHelper");

    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        MonitorMemory test = new MonitorMemory(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        int md5Result = NativeHelper.callStaticJniMethodInt(emulator, "md5(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, "xiaojianbang")); // 执行Jni方法
        System.out.println("md5Result: " + md5Result);
    }

}
