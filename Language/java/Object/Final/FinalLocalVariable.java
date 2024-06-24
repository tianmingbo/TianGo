package Object.Final;

//局部变量在定义时没有定义，那么可以赋值一次
public class FinalLocalVariable {
    public void test(final int a) {
//        a=5; 形参不能改变
    }

    public static void main(String[] args) {
        final var str = "hello";
//        str="1";
        final double f;
        //因为f没有被赋值，所以可以赋值一次
        f = 4.6;
    }
}
