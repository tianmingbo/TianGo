package Object.polymorphism;

class BaseClass {
    public int book = 6;

    public void base() {
        System.out.println("父类的普通方法");
    }

    public void test() {
        System.out.println("父类被覆盖的方法");
    }
}

public class SubClass extends BaseClass {
    public String book = "tian66";

    public void test() {
        System.out.println("覆盖父类");
    }

    public void sub() {
        System.out.println("子类中的普通方法");
    }

    public static void main(String[] args) {
        BaseClass bc = new BaseClass();
        System.out.println(bc.book);
        bc.base();
        bc.test();
        SubClass sc = new SubClass();
        System.out.println(sc.book);
        sc.test();
        sc.sub();
        /*
           编译时为BaseClass类型，运行时为SubClass类型，
           写代码的时候，只能调用编译时的类型的方法，否则会出错。
           可以强制类型转换成运行时类型
         */
        //编译时和运行时类型不一样，多态发生
        BaseClass poly = new SubClass();
        System.out.println(poly.book);
        poly.test();
        poly.base();
    }
}
