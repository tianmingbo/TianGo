package Object.innerClass;

public class StaticInnerClass {
    private int prop = 5;
    private static int prop2 = 9;

    static class StaticInner {
        private static int age;

        public void accessOuterProp() {
            //只能访问外部类的类成员
            System.out.println(prop2);
        }
    }

    public static void main(String[] args) {
        var a=new StaticInner();
        a.accessOuterProp();
    }
}
