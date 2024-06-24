package Object.fangfa;

//方法重载，方法名可以重复，只要形参列表不同就行，就是方法重载
public class overload {
    public void test() {
        System.out.println("in test");
    }

    public void test(String str) {
        System.out.println(str);
    }

    public static void main(String[] args) {
        var o = new overload();
        o.test();
        o.test("tian");
    }
}
