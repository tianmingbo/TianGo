package Object.inhertComposite;

class Animal {
    private void beat() {
        System.out.println("beat 跳动");
    }

    public void breath() {
        beat();
        System.out.println("you can breath");
    }
}

class Bird extends Animal {
    public void fly() {
        System.out.println("you can fly");
    }
}

class Wolf extends Animal {
    public void run() {
        System.out.println("you can run");
    }
}

public class Inherit {
    public static void main(String[] args) {
        var b = new Bird();
        b.fly();
        b.breath();
//        b.beat(); 父类私有方法，不可调用
        var w = new Wolf();
        w.run();
        w.breath();
    }
}
