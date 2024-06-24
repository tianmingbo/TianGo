package Object.innerClass;

class Cow {
    private double weight;
    private String prop = "outer";

    public Cow() {
    }

    public Cow(double weight) {
        this.weight = weight;
    }

    //编译为Cow$CowLeg.class
    private class CowLeg {
        /**
        * 非静态内部类里不能有静态方法，静态成员变量 ，静态初始化块
        * */
        private String prop = "inner";

        private double length;
        private String color;

        private CowLeg(double length, String color) {
            this.length = length;
            this.color = color;
        }

        public double getLength() {
            return length;
        }

        public void setLength(double length) {
            this.length = length;
        }

        public String getColor() {
            return color;
        }

        public void setColor(String color) {
            this.color = color;
        }

        public void info() {
            System.out.println("info:" + color + length + weight); //非静态内部类的成员可以访问外部类的成员。外部类访问内部类则需要显式创建非静态内部类对象
            System.out.println(this.prop);// 如果属性重名，this.访问内部类
            System.out.println(Cow.this.prop);//访问外部类
        }
    }

    public static void test2() {
        //不允许在外部类的静态成员中直接使用非静态内部类
//        new CowLeg();
    }

    public void test() {
        var cl = new CowLeg(1.12, "black");
        cl.info();
    }
}

//非静态内部类
public class NoneStaticInnerClass {

    public static void main(String[] args) {

        var cow = new Cow(333.3);
        cow.test();
    }
}
