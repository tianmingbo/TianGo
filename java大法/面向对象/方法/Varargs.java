package 面向对象.方法;

import 面向对象.Person;

//参数可变
public class Varargs {
    /**
     * 三个点表示参数数量不确定,
     * 多个参数值被当做数组传入
     * @param a
     * @param books
     */
    public static void test(int a, String... books) {
        System.out.println(a);
        for (var book : books) {
            System.out.println(book);
        }
    }

    public static void main(String[] args) {
        var p = new Person();
        p.name = "tian";
        System.out.println(p.name);
        test(12, "python", "java");
    }
}
