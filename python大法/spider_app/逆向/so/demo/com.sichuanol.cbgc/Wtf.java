package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.arm.backend.Backend;
import com.github.unidbg.arm.backend.CodeHook;
import com.github.unidbg.arm.backend.UnHook;
import com.github.unidbg.debugger.BreakPointCallback;
import com.github.unidbg.debugger.Debugger;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import unicorn.Arm64Const;
import unicorn.ArmConst;

import java.io.File;
import java.io.IOException;

public class Wtf extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass SignManager;

    private final boolean logging;

    Wtf(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.sichuanol.cbgc").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setJni(this); //接管JNI
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libwtf.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        //dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的libttEncrypt.so对应为一个模块
        SignManager = vm.resolveClass("com/sichuanol/cbgc/util/SignManager");
    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        Wtf test = new Wtf(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        //hook log输出函数,替换为nope
        emulator.getBackend().hook_add_new(new CodeHook() {
            @Override
            public void hook(Backend backend, long address, int size, Object user) {
                System.out.println(Long.toHexString(address));
                emulator.getBackend().reg_write(ArmConst.UC_ARM_REG_PC, address + 4 + 1); //修改PC寄存器地址
            }

            @Override
            public void onAttach(UnHook unHook) {
            }

            @Override
            public void detach() {
            }
        }, module.base + 0xABE, module.base + 0xABE, null);

        //利用断点方式跳过指令
//        emulator.attach().addBreakPoint(module.base + 0xABE, new BreakPointCallback() {
//            @Override
//            public boolean onHit(Emulator<?> emulator, long address) {
//                System.out.println(Long.toHexString(address));
//                emulator.getBackend().reg_write(ArmConst.UC_ARM_REG_PC, address + 4 + 1);
//                return true;
//            }
//        });

        //  修改内存中的opcode

        String data = "1636221462621";
        StringObject strResult = SignManager.callStaticJniMethodObject(emulator, "getSign(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, ""), new StringObject(vm, ""), new StringObject(vm, data)); // 执行Jni方法
        System.out.println(strResult);
    }

    @Override
    public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        if ("com/sichuanol/cbgc/util/LogShutDown->getAppSign()Ljava/lang/String;".equals(signature)) {
            return new StringObject(vm, "0093CB6721DAF15D31CFBC9BBE3A2B79");
        }
        return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
    }
}
