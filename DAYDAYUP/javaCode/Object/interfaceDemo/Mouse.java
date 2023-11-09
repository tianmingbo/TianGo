package Object.interfaceDemo;

interface USB {
    /**
     * 接口中没有构造器,没有初始化块,因为接口中没有成员变量需要初始化
     * */
    final public static int ele = 500;
    final public static int MAX_SPEED = 30 * 30 * 30;

    public abstract void in();

    //抽象方法
    public abstract void out();

    default void start() {
        System.out.println("start");
    }

    public default void end() {
        System.out.println("out");
    }

    //jdk8增加静态方法和默认方法
    public static void show() {
        System.out.println("USB 3.0 is so fast");
    }

    default double getSpeed() {
        return calculateArea();
    }

    //jdk9新增私有方法
    private double calculateArea() {
        // 面积计算的具体逻辑...
        return 0;
    }
}

public class Mouse implements USB {
    @Override
    public void in() {
        System.out.println("click");
    }

    @Override
    public void out() {
        System.out.println("screen show");
    }

    @Override
    public double getSpeed() {
        //重写默认方法.默认方法可以保留,也可以重写
        return USB.MAX_SPEED;
    }


    public static void main(String[] args) {
        Mouse mouse = new Mouse();
        mouse.in();
        mouse.out();
        System.out.println(USB.ele);
        System.out.println(USB.MAX_SPEED);
        System.out.println(mouse.getSpeed());
    }


}