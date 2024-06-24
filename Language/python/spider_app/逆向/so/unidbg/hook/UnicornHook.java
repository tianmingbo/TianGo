package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.arm.backend.Backend;
import com.github.unidbg.arm.backend.CodeHook;
import com.github.unidbg.arm.backend.UnHook;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.utils.Inspector;
import com.sun.jna.Pointer;

import javax.crypto.Cipher;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class UnicornHook extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;
    Pointer md5_ctx;

    UnicornHook(boolean logging) {
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
        UnicornHook test = new UnicornHook(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        //unicorn原生hook,inline hook
        emulator.getBackend().hook_add_new(new CodeHook() {
            //指令hook
            @Override
            public void hook(Backend backend, long address, int size, Object user) {
                RegisterContext context = emulator.getContext();
//                System.out.println("xiaojianbang");
                //System.out.println(user);
                //System.out.println(size);
                System.out.println("+++++++++++++++");
                emulator.getUnwinder().unwind(); //打印调用栈
                if (address == module.base + 0x1FF4) {
                    Pointer md5Ctx = context.getPointerArg(0);
                    Inspector.inspect(md5Ctx.getByteArray(0, 32), "md5Ctx");
                    Pointer plainText = context.getPointerArg(1);
                    int length = context.getIntArg(2);
                    Inspector.inspect(plainText.getByteArray(0, length), "plainText");
                } else if (address == module.base + 0x2004) {
                    Pointer cipherText = context.getPointerArg(1);
                    Inspector.inspect(cipherText.getByteArray(0, 16), "cipherText");
                }

            }

            @Override
            public void onAttach(UnHook unHook) {
            }

            @Override
            public void detach() {
            }
        }, module.base + 0x1FE8, module.base + 0x2004, "xiaojianbang");

        StringObject md5Result = NativeHelper.callStaticJniMethodObject(emulator, "md5(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, "xiaojianbang")); // 执行Jni方法
        System.out.println("md5Result: " + md5Result.getValue());

    }


}
