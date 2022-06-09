package Object.jicheng;

public class Override extends Bird {
    /**
     * 方法重写：
     * 要么都是类方法，要么都是实例方法
     */
    public void fly() {
        System.out.println("do not fly");
    }

    public void callOverrideMethod() {
        //super不能出现在static修饰的方法中
        super.fly();
    }

    public static void main(String[] args) {
        var os = new Override();
        os.fly();
        os.callOverrideMethod();
    }
}
