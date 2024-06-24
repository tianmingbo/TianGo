package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.Symbol;
import com.github.unidbg.arm.HookStatus;
import com.github.unidbg.arm.context.Arm32RegisterContext;
import com.github.unidbg.arm.context.Arm64RegisterContext;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.debugger.DebuggerType;
import com.github.unidbg.hook.HookContext;
import com.github.unidbg.hook.ReplaceCallback;
import com.github.unidbg.hook.hookzz.*;
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

public class Hookzz extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass NativeHelper;

    private final boolean logging;
    Pointer md5_ctx;

    Hookzz(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机

//        vm.setJni(new AbstractJni() {
//            @Override
//            public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
//                System.out.println("signature: " + signature);
//                if(signature.equals("java/lang/String->getBytes(Ljava/lang/String;)[B")) {
//                    String args = (String) dvmObject.getValue();
//                    System.out.println("args: " + args);
//                    //byte[] strBytes = args.getBytes();
//                    byte[] strBytes = "unidbg".getBytes();
//                    return new ByteArray(vm, strBytes);
//                }
//                return super.callObjectMethodV(vm, dvmObject, signature, vaList);
//            }
//        });

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
        Hookzz test = new Hookzz(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
//        IHookZz hookZz = HookZz.getInstance(emulator);
//        hookZz.wrap(module.findSymbolByName("_Z9MD5UpdateP7MD5_CTXPhj"), new WrapCallback<RegisterContext>() { // inline wrap导出函数
//            @Override
//            public void preCall(Emulator<?> emulator, RegisterContext ctx, HookEntryInfo info) {
//                md5_ctx = ctx.getPointerArg(0);
//                Pointer plainText = ctx.getPointerArg(1);
//                int length = ctx.getIntArg(2);
//                Inspector.inspect(md5_ctx.getByteArray(0, 64), "preCall md5_ctx");
//                Inspector.inspect(plainText.getByteArray(0, length), "plainText");
//            }
//            @Override
//            public void postCall(Emulator<?> emulator, RegisterContext ctx, HookEntryInfo info) {
//                Inspector.inspect(md5_ctx.getByteArray(0, 64), "postCall md5_ctx");
//            }
//        });

//        StringObject md5Result = NativeHelper.callStaticJniMethodObject(emulator, "md5(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, "xiaojianbang")); // 执行Jni方法
//        System.out.println("md5Result: " + md5Result.getValue());
        //inline hook 汇编级别hook
//        hookZz.instrument(module.base + 0x1AEC, new InstrumentCallback<Arm64RegisterContext>() {
//            @Override
//            public void dbiCall(Emulator<?> emulator, Arm64RegisterContext ctx, HookEntryInfo info) {
//                System.out.println("w8=0x" + Integer.toHexString(ctx.getXInt(8)) + ", w9=0x" + Integer.toHexString(ctx.getXInt(9)));
//            }
//        });
//
//        int retval = NativeHelper.callStaticJniMethodInt(emulator, "add(III)I", 0x100, 0x200, 0x300); // 执行Jni方法
//        System.out.println("retval: 0x" + Integer.toHexString(retval));

//        IHookZz hookZz = HookZz.getInstance(emulator);
//        hookZz.wrap(module.findSymbolByName("_Z12jstring2cstrP7_JNIEnvP8_jstring"), new WrapCallback<Arm64RegisterContext>() { // inline wrap导出函数
//            @Override
//            public void preCall(Emulator<?> emulator, Arm64RegisterContext ctx, HookEntryInfo info) {
//                //以内存写入方式传递参数，取参数时就读内存
//                //以addLocalObject方式传入Java类型参数，取参数时用getObject
//                //Pointer下有getString方法，可以直接获取内存中的字符串
//                int intArg = ctx.getIntArg(1); //取参数
//                StringObject str = vm.getObject(intArg);
//                System.out.println("preCall str = " + str.getValue());
//            }
//
//            @Override
//            public void postCall(Emulator<?> emulator, Arm64RegisterContext ctx, HookEntryInfo info) {
//                byte[] bytes = ctx.getXPointer(0).getByteArray(0, 16);
//                Inspector.inspect(bytes, "postCall cstrAddr");
//            }
//        });
//
//        Number numbers = module.callFunction(
//                emulator,
//                "_Z12jstring2cstrP7_JNIEnvP8_jstring",
//                vm.getJNIEnv(),
//                vm.addLocalObject(new StringObject(vm, "xiaojianbang")));
//        long cstrAddr = numbers.longValue();
//        byte[] bytes = emulator.getMemory().pointer(cstrAddr).getByteArray(0, 16);
//        Inspector.inspect(bytes, "cstrAddr");


        IHookZz hookZz = HookZz.getInstance(emulator);
        hookZz.wrap(module.findSymbolByName("_Z12jstring2cstrP7_JNIEnvP8_jstring"), new WrapCallback<HookZzArm64RegisterContext>() { // inline wrap导出函数
            @Override
            public void preCall(Emulator<?> emulator, HookZzArm64RegisterContext ctx, HookEntryInfo info) {
                int intArg = ctx.getIntArg(1);
                StringObject str = vm.getObject(intArg);
                System.out.println("preCall str = " + str.getValue());
            }

            @Override
            public void postCall(Emulator<?> emulator, HookZzArm64RegisterContext ctx, HookEntryInfo info) {
                String str = ctx.getXPointer(0).getString(0);
                System.out.println("postCall str: " + str);

                int hashcode = vm.addLocalObject(new StringObject(vm, "666"));
                ctx.setXLong(0, hashcode);//修改寄存器值
            }
        });

        Number numbers = module.callFunction(
                emulator,
                "_Z12jstring2cstrP7_JNIEnvP8_jstring",
                vm.getJNIEnv(),
                vm.addLocalObject(new StringObject(vm, "xiaojianbang")));
        int hashcode = numbers.intValue();
        StringObject strResult = vm.getObject(hashcode);
        System.out.println("final result: " + strResult.getValue());


    }

}
