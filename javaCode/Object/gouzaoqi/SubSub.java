package Object.gouzaoqi;

/**
 *创建任何对象总是从该类所在继承树最顶层类的构造器开始执行，
 * 然后依次向下执行，最后才会执行本类的构造器
 */
class baseAndSub {
    public baseAndSub() {
        System.out.println("无参数构造器");
    }
}

class Sub extends baseAndSub {
    public Sub(String name) {
        System.out.println("一个参数构造器" + name);
    }

    public Sub(String name, int age) {
        this(name);//调用同类中的构造器
        System.out.println("两个参数构造器" + name + ":" + age);
    }
}

public class SubSub extends Sub {

    public SubSub() {
        super("tian", 18);
        System.out.println("子类无参数构造器");
    }

    public static void main(String[] args) {
        new SubSub();
    }
}
//无参数构造器
//一个参数构造器tian
//两个参数构造器tian:18
//子类无参数构造器