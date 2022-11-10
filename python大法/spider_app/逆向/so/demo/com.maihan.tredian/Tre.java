package com.xiaojianbang;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.DvmClass;
import com.github.unidbg.linux.android.dvm.StringObject;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.utils.Inspector;

import java.io.File;
import java.io.IOException;

public class Tre {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass TreUtil;

    private final boolean logging;

    Tre(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.maihan.tredian").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/libtre.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        //dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的libttEncrypt.so对应为一个模块
        TreUtil = vm.resolveClass("com/maihan/tredian/util/TreUtil"); //定义一个对象
    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        Tre test = new Tre(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        String data = "app_ver=100&nonce=wi3nwo1632749058036&timestamp=1632749058&tzrd=BwzXzSGFyiPstMIVuzTZb7LzTZzbXRJOFzpbQiIaT7tLD0cc1eFFficAAUFoQPlbwk1GAlvWKaP4ipqRnbsFguJ0fALWPNMT6vcqr2uBwiETYt29YHmXhn+VadBnDGFnvzttJTttfKExb/bBJFSuEHKUKh+upPAGYjMNZN9hK1OdN9HxyH8Nx5BM2BnciDsQzjZLg8JAmGuHYiIUedIZaiRuUL/1np58iIU3duQ3B4KPTXvpPYb97T0ARzf8TjQp//LpfYv+QBaqNu6CBaKolV77fC1pqaR7v6eai7CIAABbWAKj6xanD+GEEDzvSTz7ZxTiZrCnAf9+0dNq7QfzbI/uf9LhD+24MshM4pcKh6FpA1PwcHH9wFWofI8dw8KCcrMdLfQ4303sA4Bp/ghN9IzBBtMIj21UAcFFgkch1iKcVTbJ8dlNWk679L7bHDutTmKSZ556wvrhtklUg9yDi0KKS/3QiNVcTXfXj+N/3T4=";
        StringObject strResult = TreUtil.callStaticJniMethodObject(emulator, "sign(Ljava/lang/String;)Ljava/lang/String;", new StringObject(vm, data)); // 执行Jni方法
        System.out.println(strResult);
    }

}
