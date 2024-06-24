package Object.InitializationBlock;

/**
 * 类初始化块在类初始化时执行，而不是创建对象时执行
 */
class Root {
    static {
        System.out.println("Root 的类初始化块");
    }

    {
        System.out.println("Root 的实例初始化块");
    }

    public Root() {
        System.out.println("root 的构造器");
    }
}

class Mid extends Root {
    static {
        System.out.println("Mid 的类初始化块");
    }

    {
        System.out.println("Mid 的实例初始化块");
    }

    public Mid() {
        System.out.println("Mid 的无参数构造器");
    }

    public Mid(String msg) {
        this();
        System.out.println("有参数构造器" + msg);
    }
}

class Leaf extends Mid {
    static {
        System.out.println("Leaf 的类初始化块");
    }

    {
        System.out.println("Leaf 的实例初始化块");
    }

    public Leaf() {
        super("tian666");
        System.out.println("执行Lead构造器");
    }

}

public class StaticInit {
    public static void main(String[] args) {
        new Leaf();
        //第一次创建Leaf对象时，因为系统中还不存在Leaf类，因此需要先加载并初始化Leaf类
        //初始化成功后，第二次就不用再创建了
        System.out.println("--------------");
        new Leaf();
    }
}
//Root 的类初始化块
//Mid 的类初始化块
//Leaf 的类初始化块
//Root 的实例初始化块
//root 的构造器
//Mid 的实例初始化块
//Mid 的无参数构造器
//有参数构造器tian666
//Leaf 的实例初始化块
//执行Lead构造器
//--------------
//Root 的实例初始化块
//root 的构造器
//Mid 的实例初始化块
//Mid 的无参数构造器
//有参数构造器tian666
//Leaf 的实例初始化块
//执行Lead构造器