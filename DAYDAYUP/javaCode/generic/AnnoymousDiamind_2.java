package generic;

interface Foo<T> {
    void test(T t);
}

//匿名内部类使用菱形语法
public class AnnoymousDiamind_2 {
    public static void main(String[] args) {
        //指定Foo类中泛型为String
        Foo<String> f = new Foo<>() {
            public void test(String t) {
                System.out.println(t);
            }
        };
        //通配符上限位object
        Foo<?> fo = new Foo<>() {
            @Override
            public void test(Object o) {
                System.out.println("object");
            }
        };
        //通配符上限位Number
        Foo<? extends Number> fn = new Foo<>() {
            @Override
            public void test(Number number) {
                System.out.println("number");
            }
        };
    }
}
