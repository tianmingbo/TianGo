package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;

/**
 * 处理so调用其它so中的方法
 */
public class NativeHelper3 extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;

    NativeHelper3(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机

        vm.setJni(this);

        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dmA = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbangA.so"), false);
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbang.so"), false);
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
        NativeHelper3 test = new NativeHelper3(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        StringObject encodeResult = NativeHelper.callStaticJniMethodObject(emulator, "encode()Ljava/lang/String;"); // 执行Jni方法
        System.out.println("encodeResult: " + encodeResult.getValue());

    }

    @Override
    public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
        System.out.println("signature: " + signature);
        if (signature.equals("java/lang/String->getBytes(Ljava/lang/String;)[B")) {
            String args = (String) dvmObject.getValue();
            System.out.println("args: " + args);
            //byte[] strBytes = args.getBytes();
            byte[] strBytes = "unidbg".getBytes();
            return new ByteArray(vm, strBytes);
        }
        return super.callObjectMethodV(vm, dvmObject, signature, vaList);
    }

}
