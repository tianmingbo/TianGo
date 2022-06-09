package Object.inhertComposite;

class Bird1 {
    //组合使用旧类对象作为新类的成员变量组合起来，用以实现新类的功能
    private final Animal a;

    public Bird1(Animal a) {
        this.a = a;
    }

    public void breath() {
        //复用animal的方法
        a.breath();
    }

    public void fly() {
        System.out.println("you can fly");
    }
}

class Wolf1 {
    //组合使用旧类对象作为新类的成员变量组合起来，用以实现新类的功能
    private final Animal a;

    public Wolf1(Animal a) {
        this.a = a;
    }

    public void breath() {
        //复用animal的方法
        a.breath();
    }

    public void run() {
        System.out.println("you can run");
    }
}

public class Composite {
    public static void main(String[] args) {
        var a1 = new Animal();
        var b = new Bird1(a1); //bird对象由animal对象组合而成
        b.breath();
        b.fly();
    }
}
