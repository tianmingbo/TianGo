package Object.innerClass;

//在外部类以外创建静态内部类实例
class StaticOut {
    static class StaticIn {
        public StaticIn() {
            System.out.println("静态内部类的构造器");
        }
    }
}

//继承
class StaticSubClass extends StaticOut.StaticIn {

}

public class CreateStaticInnerInstance {
    public static void main(String[] args) {
        //静态内部类只需要使用外部类即可调用构造器，非静态内部类必须
        //使用外部类对象来调用构造器
        StaticOut.StaticIn in = new StaticOut.StaticIn();
    }
}
