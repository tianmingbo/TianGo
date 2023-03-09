package Object.useInterface;

//接口类是一种特殊的类，一个java源文件中最多只能有一个public接口
public interface Output {
    //接口里定义的常量必须赋值，且是public static final
    int MAX_CACHE_LINE = 50;

    //接口中的普通方法默认是public的抽象(abstract)方法
    void out();

    //抽象方法
    void getData(String msg);

    //默认方法,加上default，默认使用public修饰。
    //默认方法实际上就是实例方法，接口的实现类的实例来调用
    default void print(String... msgs) {
        for (var msg : msgs) {
            System.out.println(msg);
        }
    }

    default void test() {
        System.out.println("默认的test方法");
    }

    //定义类方法，使用static修饰，接口可以直接调用
    static String staticTest() {
        return "接口里的类方法";
    }

    //定义私有方法
    private void foo() {
        System.out.println("foo 私有方法");
    }

    //定义私有静态方法
    private static void bar() {
        System.out.println("bar 私有静态方法");
    }


}
