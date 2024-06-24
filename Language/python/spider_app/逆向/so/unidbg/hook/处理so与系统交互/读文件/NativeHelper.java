package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.Symbol;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.debugger.BreakPointCallback;
import com.github.unidbg.file.FileResult;
import com.github.unidbg.file.IOResolver;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.SystemPropertyHook;
import com.github.unidbg.linux.android.SystemPropertyProvider;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.file.ByteArrayFileIO;
import com.github.unidbg.linux.file.SimpleFileIO;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.pointer.UnidbgPointer;

import java.io.*;

public class NativeHelper extends AbstractJni implements IOResolver {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass NativeHelper;
    private final boolean logging;

    NativeHelper(boolean logging) {
        this.logging = logging;
        //创建虚拟文件系统
        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.app")
                .setRootDir(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/rootfs")).build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分

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

        emulator.set("test", "dali"); //设置全局变量
        System.out.println(emulator.<Float>get("test"));

        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        emulator.getSyscallHandler().addIOResolver(this); //注册io重定向
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
        //设置环境变量
//        Symbol setenv = module.findSymbolByName("setenv", true);
//        setenv.call(emulator, "PATH", "/sbin:/system/sbin:/product/bin:/apex/com.android.runtime/bin:/system/bin:/system/xbin:/odm/bin:/vendor/bin:/vendor/xbin11111", 0);

        //hook getenv,获取环境变量时hook
        emulator.attach().addBreakPoint(module.findSymbolByName("getenv").getAddress(), new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                RegisterContext context = emulator.getContext();
                String key = context.getPointerArg(0).getString(0);
                System.out.println("xiaojianbang getenv: " + key);
                return true;
            }
        });

        NativeHelper.callStaticJniMethod(emulator, "readSomething()");
    }

    /**
     * io重定向
     */
    @Override
    public FileResult resolve(Emulator emulator, String pathname, int oflags) {
        if (("/proc/self/maps").equals(pathname)) {
            return FileResult.success(new SimpleFileIO(oflags, new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/maps"), pathname));
//            return FileResult.success(new ByteArrayFileIO(oflags, pathname, "xiaojianbangmaps".getBytes()));
        }
        //emulator.attach().debug();
        System.out.println("xiaojianbang: " + pathname);
        return null;
    }
}
