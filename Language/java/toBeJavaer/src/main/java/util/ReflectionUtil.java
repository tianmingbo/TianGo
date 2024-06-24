package util;


import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ReflectionUtil {
    /**
     * 获得调用方法的名称
     *
     * @return 方法名称
     */
    public static String getCallMethod() {
        StackTraceElement[] stack = Thread.currentThread().getStackTrace();
        // 获得调用方法名
        String method = stack[3].getMethodName();
        return method;
    }

    /**
     * 获得调用方法的类名+方法名,带上中括号
     *
     * @return 方法名称
     */
    public static String getCallClassMethod() {
        StackTraceElement stack[] = Thread.currentThread().getStackTrace();
        // 获得调用方法名
        String[] className = stack[3].getClassName().split("\\.");
//        String fullName = className[className.length - 1] + ":" + stack[3].getMethodName();
        String fullName = className[className.length - 1] + ":" + stack[3].getMethodName() + ":" + stack[3].getLineNumber();
        return fullName;
    }


    /**
     * 获得调用方法的类名+方法名
     *
     * @return 方法名称
     */
    public static String getNakeCallClassMethod() {
        StackTraceElement stack[] = Thread.currentThread().getStackTrace();
        // 获得调用方法名
        String[] className = stack[3].getClassName().split("\\.");
        String fullName = className[className.length - 1] + "." + stack[3].getMethodName();
        return fullName;
    }

    /**
     * 取得父类所有的接口
     *
     * @param targetClass
     * @return
     */
    public static Class<?>[] getInterfaces(Class<?> targetClass) {
        Set<Class<?>> interfaceSet = new HashSet<>();
        //数组转成list
        List<Class<?>> subList = Arrays.asList(targetClass.getInterfaces());
        if (subList.size() > 0) {
            interfaceSet.addAll(subList);
        }
        Class superClass = targetClass.getSuperclass();
        while (null != superClass) {
            subList = Arrays.asList(superClass.getInterfaces());

            if (subList.size() > 0) {
                interfaceSet.addAll(subList);
            }

            superClass = superClass.getSuperclass();
        }
        //set 转成 数组
        return interfaceSet.toArray(new Class<?>[0]);

    }

    public static Object newProxyInstance(Object targetObject, InvocationHandler handler) {


        Class targetClass = targetObject.getClass();

        ClassLoader loader = targetClass.getClassLoader();

        //被代理类实现的接口
        Class<?>[] targetInterfaces = ReflectionUtil.getInterfaces(targetClass);

        Object proxy = Proxy.newProxyInstance(loader, targetInterfaces, handler);
        return proxy;
    }

}


