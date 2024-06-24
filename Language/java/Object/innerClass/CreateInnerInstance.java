package Object.innerClass;

//在外部类以外创建非静态内部类
class Out {
    //没有访问控制符，只能一个包中的其他类可以访问这个内部类
    class In {
        public In(String msg) {
            System.out.println(msg);
        }
    }
}

class SubClass extends Out.In {

    public SubClass(Out out) {
        out.super("test");
    }
}

public class CreateInnerInstance {
    public static void main(String[] args) {
        //与下面三行代码功能一样
        Out.In in = new Out().new In("test");
        //创建内部类变量
        Out.In in1;
        //创建外部类实例，非静态内部类实例将寄生在该实例中
        Out out = new Out();
        //创建非静态内部类实例
        in1 = out.new In("test2");
    }
}
