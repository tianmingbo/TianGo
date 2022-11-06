package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;

/**
 * 处理so调用系统Java类
 */
public class NativeHelper2 extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;

    NativeHelper2(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        //解决jni调用java类
//        vm.setJni(new AbstractJni() {
//        });
//        vm.setJni(new AbstractJni() {
//            @Override
//            public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
//                System.out.println("signature: " + signature);
//                if(signature.equals("java/lang/String->getBytes(Ljava/lang/String;)[B")) {
//                    String args = (String) dvmObject.getValue(); //dvmObject对应java/lang/String
//                    System.out.println("args: " + args);
//                    //byte[] strBytes = args.getBytes();
//                    byte[] strBytes = "unidbg".getBytes();
//                    return new ByteArray(vm, strBytes);
//                }
//                return super.callObjectMethodV(vm, dvmObject, signature, vaList);
//            }
//        });

        vm.setJni(this); //需要继承AbstractJni

        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbang.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        //dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
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
        NativeHelper2 test = new NativeHelper2(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        StringObject md5Result = NativeHelper.callStaticJniMethodObject(emulator, "md5(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, "xiaojianbang")); // 执行Jni方法
        System.out.println("md5Result: " + md5Result.getValue());

    }

    @Override
    public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
        //复写AbstractJni中的方法
        System.out.println("signature: " + signature);
        if (signature.equals("java/lang/String->getBytes(Ljava/lang/String;)[B")) {
            //自定义处理逻辑
            String args = (String) dvmObject.getValue();
            System.out.println("args: " + args);
            //byte[] strBytes = args.getBytes();
            byte[] strBytes = "unidbg".getBytes();
            return new ByteArray(vm, strBytes);
        }
        //已经封装好的
        return super.callObjectMethodV(vm, dvmObject, signature, vaList);
    }


}
