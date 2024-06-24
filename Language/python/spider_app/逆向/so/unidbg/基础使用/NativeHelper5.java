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
import com.github.unidbg.pointer.UnidbgPointer;
import com.github.unidbg.utils.Inspector;
import com.sun.jna.Pointer;

import javax.crypto.Cipher;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * 通过偏移调用函数，32位加1.
 * 掌握操作内存
 */
public class NativeHelper5 extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;

    NativeHelper5(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setJni(this);

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
        NativeHelper5 test = new NativeHelper5(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        StringObject encodeResult = NativeHelper.callStaticJniMethodObject(emulator, "encode()Ljava/lang/String;"); // 执行Jni方法
        System.out.println("encodeResult: " + encodeResult.getValue());

        //MD5Init 2230
        UnidbgPointer MD5Ctx = emulator.getMemory().malloc(200, false).getPointer(); //MD5Ctx是结构体,因为存在内存对齐,所以直接给足够大小的内存就行.返回一个指向结构体的指针
        module.callFunction(emulator, 0x2230, MD5Ctx); //0x2230： so中的偏移地址
        //MD5Update 22A0
        UnidbgPointer plainText = emulator.getMemory().malloc(200, false).getPointer();
        byte[] buffer = "xiaojianbang_unidbg".getBytes();
        plainText.write(buffer);
        module.callFunction(emulator, 0x22A0, MD5Ctx, plainText, buffer.length);
        //MD5Final 3A78
        UnidbgPointer cipherText = emulator.getMemory().malloc(200, false).getPointer();
        module.callFunction(emulator, 0x3A78, MD5Ctx, cipherText);
        byte[] byteArray = cipherText.getByteArray(0, 16); //读数据
        Inspector.inspect(byteArray, "MD5Result");

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
