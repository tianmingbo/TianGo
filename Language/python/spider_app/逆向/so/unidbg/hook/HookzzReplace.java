package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.arm.HookStatus;
import com.github.unidbg.hook.HookContext;
import com.github.unidbg.hook.ReplaceCallback;
import com.github.unidbg.hook.hookzz.*;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import com.sun.jna.Pointer;

import java.io.File;
import java.io.IOException;

/**
 * 函数替换
 */
public class HookzzReplace extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;
    Pointer md5_ctx;

    HookzzReplace(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dmA = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbangA.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbang.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的 libxiaojianbang.so 对应为一个模块
        NativeHelper = vm.resolveClass("com/xiaojianbang/ndk/NativeHelper");

    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        HookzzReplace test = new HookzzReplace(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        IHookZz hookZz = HookZz.getInstance(emulator);
        hookZz.replace(module.findSymbolByName("Java_com_xiaojianbang_ndk_NativeHelper_md5"), new ReplaceCallback() {
            @Override
            public HookStatus onCall(Emulator<?> emulator, HookContext context, long originFunction) {
                System.out.println("onCall:123456");
                //return super.onCall(emulator, context, originFunction); //调用原函数
                //return HookStatus.RET(emulator, originFunction);//调用原函数
                return HookStatus.LR(emulator, 100); //返回100
            }

        });

        int md5Result = NativeHelper.callStaticJniMethodInt(emulator, "md5(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, "xiaojianbang")); // 执行Jni方法
        System.out.println("md5Result: " + md5Result);


    }

}
