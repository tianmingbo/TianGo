package Object.innerClass;

//匿名内部类
interface Product {
    long getPrice();

    String getName();
}

public class AnonymousTest {
    public void test(Product p) {
        System.out.println(p.getName() + p.getPrice());
    }

    public static void main(String[] args) {
        var ta = new AnonymousTest();
        //匿名内部类不能是抽象类；不能定义构造器；可以定义初始化块
        ta.test(new Product() {
            public long getPrice() {
                return 1000000000;
            }

            public String getName() {
                return "dali";
            }
        });
    }
}
