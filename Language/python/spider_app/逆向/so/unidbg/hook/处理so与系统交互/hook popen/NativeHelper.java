package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.Symbol;
import com.github.unidbg.arm.context.Arm64RegisterContext;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.debugger.BreakPointCallback;
import com.github.unidbg.file.FileResult;
import com.github.unidbg.file.IOResolver;
import com.github.unidbg.file.linux.AndroidFileIO;
import com.github.unidbg.hook.hookzz.HookZzArm64RegisterContext;
import com.github.unidbg.linux.android.*;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.file.SimpleFileIO;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.memory.MemoryBlock;
import com.github.unidbg.memory.SvcMemory;
import com.github.unidbg.pointer.UnidbgPointer;
import com.github.unidbg.unix.UnixSyscallHandler;
import unicorn.Arm64Const;
import unicorn.ArmConst;

import java.io.*;

public class NativeHelper extends AbstractJni implements IOResolver {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass NativeHelper;
    private final boolean logging;
    private int count;

    NativeHelper(boolean logging) {
        this.logging = logging;
        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app")
                .setRootDir(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/rootfs")).build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分

//        AndroidEmulatorBuilder builder = new AndroidEmulatorBuilder(true) {
//            public AndroidEmulator build() {
//                return new AndroidARM64Emulator(processName, rootDir, backendFactories) {
//                    @Override
//                    protected UnixSyscallHandler<AndroidFileIO> createSyscallHandler(SvcMemory svcMemory) {
//                        return new MySyscallHandler(svcMemory);
//                    }
//                };
//            }
//        };
//        emulator = builder.setProcessName("com.xiaojianbang.app")
//                .setRootDir(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/rootfs"))
//                .build();

        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析
        vm = emulator.createDalvikVM(); // 创建Android虚拟机

        SystemPropertyHook systemPropertyHook = new SystemPropertyHook(emulator);
        systemPropertyHook.setPropertyProvider(new SystemPropertyProvider() {
            @Override
            public String getProperty(String key) {
                System.out.println("xiaojianbang __system_property_get: " + key);
                switch (key) {

                }
                return "";
            }

            ;
        });
        memory.addHookListener(systemPropertyHook);

        GetEnvHook getEnvHook = new GetEnvHook(emulator);
        memory.addHookListener(getEnvHook);

        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        emulator.getSyscallHandler().addIOResolver(this);
        new XiaojianbangAModule(emulator, vm).register(memory);
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
        NativeHelper test = new NativeHelper(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
//        Symbol setenv = module.findSymbolByName("setenv", true);
//        setenv.call(emulator, "PATH", "/sbin:/system/sbin:/product/bin:/apex/com.android.runtime/bin:/system/bin:/system/xbin:/odm/bin:/vendor/bin:/vendor/xbin11111", 0);

        emulator.attach().addBreakPoint(module.findSymbolByName("getenv").getAddress(), new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                RegisterContext context = emulator.getContext();
                String key = context.getPointerArg(0).getString(0);
                System.out.println("xiaojianbang getenv: " + key);
                return true;
            }
        });

        emulator.attach().addBreakPoint(module.findSymbolByName("popen").getAddress(), new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                RegisterContext context = emulator.getContext();
                String command = context.getPointerArg(0).getString(0);
                System.out.println("popen command: " + command);
                return true;
            }
        });

        // BL .popen
        emulator.attach().addBreakPoint(module.base + 0x26E4, new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                emulator.getBackend().reg_write(Arm64Const.UC_ARM64_REG_PC, address + 4);
                return true;
            }
        });

        // BL .__fgets_chk
        emulator.attach().addBreakPoint(module.base + 0x2744, new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                emulator.getBackend().reg_write(Arm64Const.UC_ARM64_REG_PC, address + 4);
                return true;
            }
        });
        // CBZ X8, loc_27EC 第一次x8不为0，第二次为0
        emulator.attach().addBreakPoint(module.base + 0x276C, new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                if (count == 0) {
                    count = 1;
                    System.out.println("while is run 0");
                } else if (count == 1) {
                    emulator.getBackend().reg_write(Arm64Const.UC_ARM64_REG_X8, 0);
                    System.out.println("while is run 1");
                }
                //emulator.getBackend().reg_write(Arm64Const.UC_ARM64_REG_PC, address + 4);
                return true;
            }
        });

        NativeHelper.callStaticJniMethod(emulator, "readSomething()");
    }

    @Override
    public FileResult resolve(Emulator emulator, String pathname, int oflags) {
        if (("/proc/self/maps").equals(pathname)) {
            return FileResult.success(new SimpleFileIO(oflags, new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/maps"), pathname));
            //return FileResult.success(new ByteArrayFileIO(oflags, pathname, "xiaojianbangmaps".getBytes()));
        }
        //emulator.attach().debug();
        System.out.println("xiaojianbang: " + pathname);
        return null;
    }
}
