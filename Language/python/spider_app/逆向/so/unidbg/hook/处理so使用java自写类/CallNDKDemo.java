package com.xiaojianbang.ndk;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ArrayObject;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.linux.android.dvm.array.IntArray;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;

/**
 * dvmObject是一个对象或类,
 * (NDKDemo) dvmObject.getValue(); 转成NDKDemo类型的对象
 * VM的resolveClass方法会创建出一个类型，可以理解为Java中的一个类
 */
public class CallNDKDemo extends AbstractJni {

    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;

    private final DvmClass MainActivity;

    private final boolean logging;

    CallNDKDemo(boolean logging) {
        this.logging = logging;

        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.xiaojianbang.ndkdemo").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        memory.setLibraryResolver(new AndroidResolver(23)); // 设置系统类库解析

        vm = emulator.createDalvikVM(); // 创建Android虚拟机
        vm.setJni(this);
        vm.setVerbose(logging); // 设置是否打印Jni调用细节
        DalvikModule dmB = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbangB.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        DalvikModule dm = vm.loadLibrary(new File("unidbg-android/src/test/java/com/xiaojianbang/ndk/libxiaojianbangA.so"), false); // 加载libttEncrypt.so到unicorn虚拟内存，加载成功以后会默认调用init_array等函数
        dm.callJNI_OnLoad(emulator); // 手动执行JNI_OnLoad函数
        module = dm.getModule(); // 加载好的libttEncrypt.so对应为一个模块
        MainActivity = vm.resolveClass("com/xiaojianbang/ndkdemo/MainActivity");
    }

    void destroy() throws IOException {
        emulator.close();
        if (logging) {
            System.out.println("destroy");
        }
    }

    public static void main(String[] args) throws Exception {
        CallNDKDemo test = new CallNDKDemo(true);
        test.callFunc();
        test.destroy();
    }

    void callFunc() {
        StringObject strResult = MainActivity.callStaticJniMethodObject(emulator, "testJniFunc()Ljava/lang/String;"); // 执行Jni方法
        System.out.println(strResult.getValue());
    }

    @Override
    public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
        if ("java/lang/Class->getClassLoader()Ljava/lang/ClassLoader;".equals(signature)) {
            return vm.resolveClass("java/lang/ClassLoader").newObject(null);
        } else if ("com/xiaojianbang/ndkdemo/NDKDemo->privateFunc(Ljava/lang/String;I)Ljava/lang/String;".equals(signature)) {
            NDKDemo ndkDemo = (NDKDemo) dvmObject.getValue();
            StringObject str = vaList.getObjectArg(0); //获取第一个参数
            int nums = vaList.getIntArg(1);//获取第二个参数
            return new StringObject(vm, ndkDemo.privateFunc(str.getValue(), nums));
        }
        return super.callObjectMethodV(vm, dvmObject, signature, vaList);
    }

    @Override
    public DvmObject<?> allocObject(BaseVM vm, DvmClass dvmClass, String signature) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->allocObject".equals(signature)) {
            return vm.resolveClass("com/xiaojianbang/ndkdemo/NDKDemo").newObject(null);
        }
        return super.allocObject(vm, dvmClass, signature);
    }

    @Override
    public DvmObject<?> newObjectV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo-><init>(Ljava/lang/String;I)V".equals(signature)) {
            StringObject str = vaList.getObjectArg(0);
            int nums = vaList.getIntArg(1);
            NDKDemo ndkDemo = new NDKDemo(str.getValue(), nums);//
            return vm.resolveClass("com/xiaojianbang/ndkdemo/NDKDemo").newObject(ndkDemo);
        }
        return super.newObjectV(vm, dvmClass, signature, vaList);
    }

    @Override
    public DvmObject<?> getStaticObjectField(BaseVM vm, DvmClass dvmClass, String signature) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->privateStaticStringField:Ljava/lang/String;".equals(signature)) {
            return new StringObject(vm, NDKDemo.privateStaticStringField);
        }
        return super.getStaticObjectField(vm, dvmClass, signature);
    }

    @Override
    public void setObjectField(BaseVM vm, DvmObject<?> dvmObject, String signature, DvmObject<?> value) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->privateStringField:Ljava/lang/String;".equals(signature)) {
            NDKDemo ndkDemo = (NDKDemo) dvmObject.getValue(); //创建一个对象
            ndkDemo.privateStringField = (String) value.getValue(); //修改值
            return; //return退出,避免走下面流程
        }
        super.setObjectField(vm, dvmObject, signature, value);
    }

    @Override
    public DvmObject<?> getObjectField(BaseVM vm, DvmObject<?> dvmObject, String signature) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->privateStringField:Ljava/lang/String;".equals(signature)) {
            NDKDemo ndkDemo = (NDKDemo) dvmObject.getValue();
            return new StringObject(vm, ndkDemo.privateStringField);
        } else if ("com/xiaojianbang/ndkdemo/NDKDemo->byteArray:[B".equals(signature)) {
            NDKDemo ndkDemo = (NDKDemo) dvmObject.getValue();
            return new ByteArray(vm, ndkDemo.byteArray);
        }
        return super.getObjectField(vm, dvmObject, signature);
    }

    @Override
    public void callStaticVoidMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->publicStaticFunc()V".equals(signature)) {
            NDKDemo.publicStaticFunc();
            return;
        }
        super.callStaticVoidMethodV(vm, dvmClass, signature, vaList);
    }

    @Override
    public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        if ("com/xiaojianbang/ndkdemo/NDKDemo->privateStaticFunc([Ljava/lang/String;)[I".equals(signature)) {
            //[Ljava/lang/String 字符串数组
            ArrayObject arrayObject = vaList.getObjectArg(0); //取第一个参数
            DvmObject[] stringArrayObj = arrayObject.getValue();
            String[] stringArray = new String[stringArrayObj.length]; //取字符串数组参数
            for (int i = 0; i < stringArray.length; i++) {
                stringArray[i] = (String) stringArrayObj[i].getValue();
            }
            System.out.println(Arrays.toString(stringArray));
            return new IntArray(vm, NDKDemo.privateStaticFunc(stringArray));
        }
        return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
    }
}
