package Object.lambda;

interface Eatable {
    void taste();
}

interface Flyable {
    void fly(String weather);
}

interface Addable {
    int add(int a, int b);
}

public class LambdaQs {
    public void eat(Eatable e) {
        System.out.println(e);
        e.taste();
    }

    public void drive(Flyable f) {
        System.out.println("drive:" + f);
    }

    public void test(Addable add) {
        System.out.println(add.add(5, 3));
    }

    public static void main(String[] args) {
        var lq = new LambdaQs();
        //代码块只有一行,省略花括号
        lq.eat(() -> System.out.println("apple taste nice"));
        //只有一个形参,省略圆括号
        lq.drive(weather -> {
            System.out.println("weather is:" + weather);
        });
        //只有一条语句,即时该表达式需要返回值,也可以省略return
        lq.test((a, b) -> a + b);
    }
}
