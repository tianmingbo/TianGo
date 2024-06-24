package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.debugger.BreakPointCallback;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import unicorn.ArmConst;

import java.io.File;
import java.io.IOException;

public class Mfw extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass AuthorizeHelper;

    private final boolean logging;

    Mfw(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.mfw.roadbook").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libmfw.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        //dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的libttEncrypt.so对应为一个模块
        AuthorizeHelper = vm.resolveClass("com/mfw/tnative/AuthorizeHelper");
    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        Mfw test = new Mfw(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        //跳过0x914C
        emulator.attach().addBreakPoint(module.base + 0x914C, new BreakPointCallback() {
            @Override
            public boolean onHit(Emulator<?> emulator, long address) {
                emulator.getBackend().reg_write(ArmConst.UC_ARM_REG_PC, address + 4 + 1);
                emulator.getBackend().reg_write(ArmConst.UC_ARM_REG_R0, 1);
                return true;
            }
        });

        String data = "PUT&https%3A%2F%2Fmapi.mafengwo.cn%2Frest%2Fapp%2Fuser%2Flogin%2F&after_style%3Ddefault%26app_code%3Dcom.mfw.roadbook%26app_ver%3D8.1.6%26app_version_code%3D535%26brand%3Dgoogle%26channel_id%3DGROWTH-WAP-LC-3%26device_id%3DAC%253A37%253A43%253AA9%253A3F%253A34%26device_type%3Dandroid%26hardware_model%3DPixel%26mfwsdk_ver%3D20140507%26oauth_consumer_key%3D5%26oauth_nonce%3Dcfa857ff-8f4c-4268-8c75-37f07c7aaccf%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1632795895%26oauth_version%3D1.0%26open_udid%3DAC%253A37%253A43%253AA9%253A3F%253A34%26put_style%3Ddefault%26screen_height%3D1794%26screen_scale%3D2.625%26screen_width%3D1080%26sys_ver%3D10%26time_offset%3D480%26x_auth_mode%3Dclient_auth%26x_auth_password%3Da12345678%26x_auth_username%3D15968079477";
        StringObject strResult = AuthorizeHelper.callStaticJniMethodObject(
                emulator,
                "xAuthencode(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)Ljava/lang/String;",
                vm.addLocalObject(vm.resolveClass("android/content/Context")),
                new StringObject(vm, data),
                new StringObject(vm, ""),
                new StringObject(vm, "com.mfw.roadbook"),
                true
        ); // 执行Jni方法
        System.out.println(strResult);
    }

}
