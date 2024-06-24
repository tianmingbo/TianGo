package com.xiaojianbang.ndk;

import com.github.unidbg.Emulator;
import com.github.unidbg.arm.Arm64Svc;
import com.github.unidbg.arm.ArmSvc;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.memory.SvcMemory;
import com.github.unidbg.pointer.UnidbgPointer;
import com.github.unidbg.virtualmodule.VirtualModule;

import java.util.Map;

//自定义module
public class XiaojianbangAModule extends VirtualModule<VM> {

    public XiaojianbangAModule(Emulator<?> emulator, VM vm) {
        super(emulator, vm, "libxiaojianbangA.so");
    }

    @Override
    protected void onInitialize(Emulator<?> emulator, final VM vm, Map<String, UnidbgPointer> symbols) {
        boolean is64Bit = emulator.is64Bit();
        SvcMemory svcMemory = emulator.getSvcMemory();
        symbols.put("_Z7bssFuncv", svcMemory.registerSvc(is64Bit ? new Arm64Svc() {
            @Override
            public long handle(Emulator<?> emulator) {
                fromJava(emulator, vm);
                return 0;
            }
        } : new ArmSvc() {
            @Override
            public long handle(Emulator<?> emulator) {
                fromJava(emulator, vm);
                return 0;
            }
        }));

    }

    private static void fromJava(Emulator<?> emulator, VM vm) {
        System.out.println("libxiaojianbangA.so");
    }

}
