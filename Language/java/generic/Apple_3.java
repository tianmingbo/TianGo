package generic;


//可以为任何类，接口增加泛型声明（并不是只有集合类才可以使用泛型）
class Apple<T> {
    private T info; //T 类型

    /*
     * 不管泛型的实际类型参数是什么，他们在运行时总有同样的类。
     * 因此静态方法、静态初始化块、或者静态变量的声明和初始化中不允许使用泛型形参
     * */
    //    static T info2;
    public Apple(T info) {
        this.info = info;
    }

    public void setInfo(T info) {
        this.info = info;
    }

    public T getInfo() {
        return this.info;
    }
}

class Apple2 extends Apple<String> {
    public Apple2(String info) {
        super(info);
    }

    public String getInfo() {
        return "subClass" + super.getInfo();
    }
}

public class Apple_3 {
    public static void main(String[] args) {
        //T 的形参是String
        Apple<String> a1 = new Apple<>("apple");
        a1.setInfo("banana");
        System.out.println(a1.getInfo());
        //T 的形参是Double类型
        Apple<Double> a2 = new Apple<>(3.33);
        System.out.println(a2.getInfo());
    }
}
