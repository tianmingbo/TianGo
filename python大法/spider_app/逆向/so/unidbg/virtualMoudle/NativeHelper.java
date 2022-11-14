package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;

import java.io.*;

public class NativeHelper extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass NativeHelper;
    private final boolean logging;

    NativeHelper(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机

        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节

        new XiaojianbangAModule(emulator, vm).register(memory); //注册自定义的虚拟模块,避免依赖

        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbang.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        module = dm.getModule(); // 加载好的 libxiaojianbang.so 对应为一个模块

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
        NativeHelper test = new NativeHelper(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        int retval = NativeHelper.callStaticJniMethodInt(emulator, "add(III)I", 0x100, 0x200, 0x300); // 执行Jni方法
        System.out.println("retval: 0x" + Integer.toHexString(retval));
    }

}
