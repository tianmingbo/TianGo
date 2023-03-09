package Object.classMember;

class Singleton {
    //使用类变量存储已经创建过的实例
    private static Singleton instance;

    //使用private隐藏构造器
    private Singleton() {
    }

    public static Singleton getInstance() {
        //如果instance为null，则创建实例
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}

public class SingletonTest {
    public static void main(String[] args) {
        //单例模式，只能创建一个对象
        var s1 = Singleton.getInstance();
        var s2 = Singleton.getInstance();
        System.out.println(s1 == s2);
    }
}
