package com.xiaojianbang.ndk;

import com.github.unidbg.Emulator;
import com.github.unidbg.arm.Arm64Hook;
import com.github.unidbg.arm.ArmHook;
import com.github.unidbg.arm.HookStatus;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.hook.HookListener;
import com.github.unidbg.memory.SvcMemory;
import com.sun.jna.Pointer;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


public class GetEnvHook implements HookListener {

    private final Emulator<?> emulator;

    public GetEnvHook(Emulator<?> emulator) {
        this.emulator = emulator;
    }

    @Override
    public long hook(SvcMemory svcMemory, String libraryName, String symbolName, final long old) {
        if ("libc.so".equals(libraryName)) {
            if ("getenv".equals(symbolName)) {
                if (emulator.is64Bit()) {
                    return svcMemory.registerSvc(new Arm64Hook() {
                        @Override
                        protected HookStatus hook(Emulator<?> emulator) {
                            RegisterContext context = emulator.getContext();
                            int index = 0;
                            Pointer pointer = context.getPointerArg(index);
                            String key = pointer.getString(0);
                            System.out.println("Hook: " + key);
                            return HookStatus.RET(emulator, old);
                        }
                    }).peer;
                } else {
                    return svcMemory.registerSvc(new ArmHook() {
                        @Override
                        protected HookStatus hook(Emulator<?> emulator) {
                            RegisterContext context = emulator.getContext();
                            int index = 0;
                            Pointer pointer = context.getPointerArg(index);
                            String key = pointer.getString(0);
                            System.out.println("Hook: " + key);
                            return HookStatus.RET(emulator, old);
                        }
                    }).peer;
                }
            }

        }
        return 0;
    }
}
