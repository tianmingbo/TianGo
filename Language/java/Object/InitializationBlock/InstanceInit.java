package Object.InitializationBlock;

public class InstanceInit {
    {
        var a = 6;
        System.out.println(a);
        System.out.println("实例初始化块");
    }

    {
        System.out.println("第二个实例初始化块");
    }

    public InstanceInit() {
        System.out.println("构造器");
    }

    public static void main(String[] args) {
        //实例初始化块只在创建Java对象时隐式执行，
        //而且是在构造器执行之前自动执行
        new InstanceInit();
    }
}
//6
//实例初始化块
//第二个实例初始化块
//构造器