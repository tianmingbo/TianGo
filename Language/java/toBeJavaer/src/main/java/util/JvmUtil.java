package util;

import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.lang.reflect.Type;


public class JvmUtil
{

    public static final long getMxMemory()
    {
        return   Runtime.getRuntime().maxMemory();
    }

    /**
     * 获取进程id
     * @return  进程id
     */
    public static final int getProcessID()
    {
        //  ManagementFactory是一个在运行时管理和监控Java VM的工厂类
        //  它能提供很多管理VM的静态接口的运行时实例，比如RuntimeMXBean
        //  RuntimeMXBean是Java虚拟机的运行时管理接口.
        //  取得VM运行管理实例，到管理接口句柄
        RuntimeMXBean runtimeMXBean = ManagementFactory.getRuntimeMXBean();
        //  取得VM运行管理实例的名称，也是JVM运行实例的名称
        String jvmInstanceName = runtimeMXBean.getName();
        return Integer.valueOf(jvmInstanceName.split("@")[0]).intValue();
    }


    public static void main(String[] args) {
        System.out.println("getMxMemory() = " + getMxMemory() /1024/1024/1024+" G");
    }

    public static boolean isWin() {
        String os = System.getProperty("os.name");
        if(os.toLowerCase().startsWith("win")){
            return  true;
        }
        return  false;
    }

    public static boolean isClassPresent(String className) {
        try {
            Class.forName(className);
            return true;
        } catch (IllegalAccessError err) {
            throw new IllegalStateException("Readability mismatch in inheritance hierarchy of class [" +
                    className + "]: " + err.getMessage(), err);
        } catch (Throwable ex) {
            // Typically ClassNotFoundException or NoClassDefFoundError...
            return false;
        }
    }

    public static  Type getType(Object object) {

        //new后面带上大括号，表示重写父类方法，创建了一个匿名子类
//        Map<String,String> model = new HashMap<String,String>(){};
//        Type type= model.getClass().getGenericSuperclass();

        return object.getClass().getGenericSuperclass();
    }

    public static final String OS_NAME = System.getProperty("os.name");
    private static boolean isLinuxPlatform = false;
    private static boolean isWindowsPlatform = false;
    static {
        if (OS_NAME != null && OS_NAME.toLowerCase().contains("linux")) {
            isLinuxPlatform = true;
        }

        if (OS_NAME != null && OS_NAME.toLowerCase().contains("windows")) {
            isWindowsPlatform = true;
        }

    }
    public static boolean isLinuxPlatform() {
        return false;
    }



}
