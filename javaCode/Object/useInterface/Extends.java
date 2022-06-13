package Object.useInterface;

interface InterfaceA {
    int PROP_A = 5;

    void testA();
}

interface InterfaceB {
    int PROP_B = 6;

    void testB();
}

//可以多继承
interface InterfaceC extends InterfaceA, InterfaceB {
    int PROP_C = 7;

    static void test() {
        System.out.println("in test");
    }

    void testC();
}

public interface Extends {
    public static void main(String[] args) {
        InterfaceC.test();
        System.out.println(InterfaceC.PROP_A);
        System.out.println(InterfaceC.PROP_B);
        System.out.println(InterfaceC.PROP_C);
    }
}
