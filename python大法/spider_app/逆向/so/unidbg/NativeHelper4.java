package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.Symbol;
import com.github.unidbg.arm.HookStatus;
import com.github.unidbg.arm.context.Arm32RegisterContext;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.debugger.DebuggerType;
import com.github.unidbg.hook.HookContext;
import com.github.unidbg.hook.ReplaceCallback;
import com.github.unidbg.hook.hookzz.Dobby;
import com.github.unidbg.hook.hookzz.HookEntryInfo;
import com.github.unidbg.hook.hookzz.HookZz;
import com.github.unidbg.hook.hookzz.IHookZz;
import com.github.unidbg.hook.hookzz.InstrumentCallback;
import com.github.unidbg.hook.hookzz.WrapCallback;
import com.github.unidbg.hook.xhook.IxHook;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.XHookImpl;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.utils.Inspector;
import com.sun.jna.Pointer;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * 通过符号调用函数
 */
public class NativeHelper4 extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;

    NativeHelper4(boolean logging) {
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
        NativeHelper4 test = new NativeHelper4(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {

//        Symbol symbol = module.findSymbolByName("Java_com_xiaojianbang_ndk_NativeHelper_add");
//        if (symbol != null) {
//            Number numbers = symbol.call(emulator, vm.getJNIEnv(), vm.addLocalObject(NativeHelper), 100, 200, 300); //vm.addLocalObject(NativeHelper)：jclass
//            int result = numbers.intValue();
//            System.out.println(result);
//        } else {
//            System.out.println("符号未找到");
//        }


        Symbol symbol = module.findSymbolByName("_Z7_strcatP7_JNIEnvP7_jclass"); //so中出现的名字
        Number numbers = symbol.call(emulator, vm.getJNIEnv(), vm.addLocalObject(NativeHelper));
        int result = numbers.intValue();
        System.out.println(vm.getObject(result).getValue());

//        Number[] numbers = module.callFunction(emulator, "_Z7_strcatP7_JNIEnvP7_jclass", vm.getJNIEnv(), vm.addLocalObject(NativeHelper));
//        int result = numbers[0].intValue();
//        System.out.println(vm.getObject(result).getValue());
//
//        DvmObject obj = NativeHelper.newObject(null);
//        System.out.println(vm.addLocalObject(obj));
//        System.out.println(obj.hashCode());


    }


}
